import logging
from typing import Any, Dict, List, Optional

from application.ports.metabase_gateway import MetabaseGateway
from application.schemas import DashboardCreatePayload, DashboardCopyPayload, DashboardUpdatePayload
from domain.models import DashboardCard, DashboardTab, EmbeddingParams

logger = logging.getLogger("metabase-mcp")

# Fields accepted by PUT /api/dashboard/:id/cards. The GET response embeds
# a full nested `card` object (with result_metadata, dataset_query, etc.) that
# Metabase rejects when echoed back — sending it causes a transaction abort (500).
_DASHCARD_PUT_FIELDS = frozenset({
    "id", "card_id", "row", "col", "size_x", "size_y",
    "series", "parameter_mappings", "visualization_settings",
    "dashboard_tab_id", "action_id", "inline_parameters",
})

# Optional dashcard fields that should be omitted from the payload when None,
# instead of sent as null. `card_id` is intentionally NOT here: virtual cards
# (heading/text/link) legitimately carry card_id=null and must keep it.
_DROP_IF_NONE = {"dashboard_tab_id", "inline_parameters"}


def _strip_for_put(c: Dict[str, Any]) -> Dict[str, Any]:
    """Strip a raw GET dashcard to only the fields accepted by PUT /api/dashboard/:id.

    The GET response embeds nested objects that Metabase rejects in PUT:
    - `card`: full card object (result_metadata, dataset_query, etc.) → dropped entirely
    - `series`: full card objects → normalized to [{id: card_id}] minimal references
    - `visualization_settings.virtual_card`: may contain complex internal Metabase fields
      (dataset_query with Clojure fn references, etc.) → stripped to minimal display format
    Sending these verbatim causes a Postgres transaction abort (500).
    """
    result = {k: v for k, v in c.items() if k in _DASHCARD_PUT_FIELDS}

    # Normalize series to minimal card references
    if result.get("series"):
        result["series"] = [
            {"id": s["id"]} for s in result["series"]
            if isinstance(s, dict) and "id" in s
        ]

    # For virtual cards (heading/text/link), strip the nested virtual_card object
    # to minimal safe format. The GET embeds internal fields inside virtual_card
    # (complex dataset_query, fn references, etc.) that the PUT rejects.
    if result.get("card_id") is None:
        viz = result.get("visualization_settings") or {}
        vc = viz.get("virtual_card")
        if vc:
            result["visualization_settings"] = {
                **{k: v for k, v in viz.items() if k != "virtual_card"},
                "virtual_card": {
                    "display": vc.get("display"),
                    "name": vc.get("name"),
                    "visualization_settings": {},
                    "dataset_query": {},
                },
            }

    # Drop optional None fields (same logic as _DROP_IF_NONE)
    for field in _DROP_IF_NONE:
        if result.get(field) is None:
            result.pop(field, None)
    return result


def _summarize_dashcard(c: Dict[str, Any]) -> Dict[str, Any]:
    """Trim a raw dashcard to the fields needed to operate (drops the huge `card` object)."""
    card = c.get("card") or {}
    name = card.get("name")
    if name is None:
        vs = c.get("visualization_settings") or {}
        name = vs.get("text") or (vs.get("virtual_card") or {}).get("display")
    return {
        "id": c.get("id"),
        "card_id": c.get("card_id"),
        "name": name,
        "dashboard_tab_id": c.get("dashboard_tab_id"),
        "row": c.get("row"),
        "col": c.get("col"),
        "size_x": c.get("size_x"),
        "size_y": c.get("size_y"),
    }


def _summarize_dashboard(d: Dict[str, Any]) -> Dict[str, Any]:
    """Trim a full dashboard object to id/name/tabs + summarized dashcards."""
    return {
        "id": d.get("id"),
        "name": d.get("name"),
        "collection_id": d.get("collection_id"),
        "tabs": [{"id": t.get("id"), "name": t.get("name")} for t in (d.get("tabs") or [])],
        "dashcards": [_summarize_dashcard(c) for c in (d.get("dashcards") or [])],
    }


class DashboardService:
    """Use cases for Metabase dashboards (`/api/dashboard`)."""

    def __init__(self, gateway: MetabaseGateway) -> None:
        self._gw = gateway

    async def list_dashboards(self) -> Dict[str, Any]:
        return await self._gw.get("/api/dashboard")

    async def get_by_id(self, dashboard_id: int, summary: bool = False) -> Dict[str, Any]:
        dashboard = await self._gw.get(f"/api/dashboard/{dashboard_id}")
        return _summarize_dashboard(dashboard) if summary else dashboard

    async def get_cards(self, dashboard_id: int, summary: bool = False) -> Dict[str, Any]:
        """
        There is no `GET /api/dashboard/:id/cards` endpoint; the dashcards live
        inside the dashboard object, so fetch the dashboard and return them.
        """
        dashboard = await self._gw.get(f"/api/dashboard/{dashboard_id}")
        dashcards = dashboard.get("dashcards", []) or []
        if summary:
            dashcards = [_summarize_dashcard(c) for c in dashcards]
        return {"data": dashcards, "count": len(dashcards)}

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        collection_id: Optional[int] = None,
        parameters: Optional[List] = None,
        tabs: Optional[List[Dict[str, str]]] = None,
        cache_ttl: Optional[int] = None,
        collection_position: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload = DashboardCreatePayload(
            name=name,
            description=description,
            collection_id=collection_id,
            parameters=parameters,
            tabs=tabs,
            cache_ttl=cache_ttl,
            collection_position=collection_position,
        ).model_dump(exclude_none=True)
        logger.info(f"Creating dashboard '{name}'")
        return await self._gw.post("/api/dashboard", json=payload)

    async def _put_dashcards(
        self,
        dashboard_id: int,
        dashcards_raw: List[Dict[str, Any]],
        tabs: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        PUT the dashcards (and tabs) via PUT /api/dashboard/:id/cards.
        Tabs MUST be included in the payload — without them, Metabase deletes all
        dashboard_tab rows for the dashboard, causing FK constraint failures on insert.
        Raw GET dashcards are stripped to PUT-safe fields. Broken virtual cards
        (card_id=null without virtual_card settings) are dropped.
        """
        cleaned = []
        for c in dashcards_raw:
            stripped = _strip_for_put(c)
            if stripped.get("card_id") is None:
                # Keep only legitimate virtual cards (text/heading/link widgets)
                viz = c.get("visualization_settings") or {}
                if not viz.get("virtual_card"):
                    logger.warning(
                        f"Dropping broken dashcard id={stripped.get('id')} "
                        f"(card_id=null, no virtual_card) from dashboard {dashboard_id}"
                    )
                    continue
            cleaned.append(stripped)

        payload: Dict[str, Any] = {"cards": cleaned}
        if tabs:
            payload["tabs"] = [{"id": t["id"], "name": t.get("name", "")} for t in tabs]

        return await self._gw.put(f"/api/dashboard/{dashboard_id}/cards", json=payload)

    async def update(
        self,
        dashboard_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        collection_id: Optional[int] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
        tabs: Optional[List[DashboardTab]] = None,
        dashcards: Optional[List[DashboardCard]] = None,
        points_of_interest: Optional[str] = None,
        caveats: Optional[str] = None,
        enable_embedding: Optional[bool] = None,
        embedding_params: Optional[EmbeddingParams] = None,
        archived: Optional[bool] = None,
        position: Optional[int] = None,
        collection_position: Optional[int] = None,
        cache_ttl: Optional[int] = None,
        width: Optional[str] = None,
        show_in_getting_started: Optional[bool] = None,
    ) -> Dict[str, Any]:
        # Partial update: only send the fields actually provided. Metabase preserves
        # everything we don't send (including the existing dashcards/tabs when omitted),
        # so there's no need to fetch-and-echo the whole object (which also avoids
        # re-sending null fields that Metabase rejects on sparsely-populated dashboards).
        payload = DashboardUpdatePayload(
            name=name,
            description=description,
            collection_id=collection_id,
            parameters=parameters,
            tabs=tabs,
            dashcards=dashcards,
            points_of_interest=points_of_interest,
            caveats=caveats,
            enable_embedding=enable_embedding,
            embedding_params=embedding_params,
            archived=archived,
            position=position,
            collection_position=collection_position,
            cache_ttl=cache_ttl,
            width=width,
            show_in_getting_started=show_in_getting_started,
        ).model_dump(exclude_none=True)

        if not payload:
            # Nothing to change; return current state instead of an empty PUT.
            return await self._gw.get(f"/api/dashboard/{dashboard_id}")

        logger.info(f"Updating dashboard {dashboard_id}")
        return await self._gw.put(f"/api/dashboard/{dashboard_id}", json=payload)

    async def add_card(
        self,
        dashboard_id: int,
        card_id: int,
        row: int,
        col: int,
        size_x: int,
        size_y: int,
        dashboard_tab_id: Optional[int] = None,
        series: Optional[List[Dict[str, Any]]] = None,
        parameter_mappings: Optional[List[Dict[str, Any]]] = None,
        visualization_settings: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Append a single card to a dashboard, preserving all existing dashcards."""
        existing = await self._gw.get(f"/api/dashboard/{dashboard_id}")
        current = existing.get("dashcards", []) or []
        tabs = existing.get("tabs", []) or []

        new_card = DashboardCard(
            id=-1,
            card_id=card_id,
            row=row,
            col=col,
            size_x=size_x,
            size_y=size_y,
            series=series or [],
            parameter_mappings=parameter_mappings or [],
            visualization_settings=visualization_settings or {},
            dashboard_tab_id=dashboard_tab_id,
        ).model_dump()

        logger.info(f"Adding card {card_id} to dashboard {dashboard_id}")
        return await self._put_dashcards(dashboard_id, current + [new_card], tabs=tabs)

    async def remove_card(self, dashboard_id: int, dashcard_id: int) -> Dict[str, Any]:
        """Remove a single dashcard (by its dashcard id) preserving the rest."""
        existing = await self._gw.get(f"/api/dashboard/{dashboard_id}")
        current = existing.get("dashcards", []) or []
        tabs = existing.get("tabs", []) or []
        new_list = [c for c in current if c.get("id") != dashcard_id]
        if len(new_list) == len(current):
            raise ValueError(f"dashcard {dashcard_id} not found in dashboard {dashboard_id}")
        logger.info(f"Removing dashcard {dashcard_id} from dashboard {dashboard_id}")
        return await self._put_dashcards(dashboard_id, new_list, tabs=tabs)

    async def move_resize_card(
        self,
        dashboard_id: int,
        dashcard_id: int,
        row: Optional[int] = None,
        col: Optional[int] = None,
        size_x: Optional[int] = None,
        size_y: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Change position/size of one dashcard, leaving every other field and card intact."""
        existing = await self._gw.get(f"/api/dashboard/{dashboard_id}")
        current = existing.get("dashcards", []) or []
        tabs = existing.get("tabs", []) or []
        found = False
        for c in current:
            if c.get("id") == dashcard_id:
                if row is not None:
                    c["row"] = row
                if col is not None:
                    c["col"] = col
                if size_x is not None:
                    c["size_x"] = size_x
                if size_y is not None:
                    c["size_y"] = size_y
                found = True
                break
        if not found:
            raise ValueError(f"dashcard {dashcard_id} not found in dashboard {dashboard_id}")
        logger.info(f"Moving/resizing dashcard {dashcard_id} on dashboard {dashboard_id}")
        return await self._put_dashcards(dashboard_id, current, tabs=tabs)

    async def delete(self, dashboard_id: int) -> Dict[str, Any]:
        logger.info(f"Deleting dashboard {dashboard_id}")
        return await self._gw.delete(f"/api/dashboard/{dashboard_id}")

    async def copy(
        self,
        from_dashboard_id: int,
        name: str,
        description: Optional[str] = None,
        collection_id: Optional[int] = None,
        is_deep_copy: bool = False,
        collection_position: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload = DashboardCopyPayload(
            name=name,
            description=description,
            collection_id=collection_id,
            is_deep_copy=is_deep_copy,
            collection_position=collection_position,
        ).model_dump(exclude_none=True)
        logger.info(f"Copying dashboard {from_dashboard_id} to '{name}'")
        return await self._gw.post(f"/api/dashboard/{from_dashboard_id}/copy", json=payload)

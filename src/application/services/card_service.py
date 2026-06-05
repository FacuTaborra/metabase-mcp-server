import logging
from typing import Any, Dict, List, Optional, Union

from application.ports.metabase_gateway import MetabaseGateway
from application.schemas import CardCreatePayload, CardUpdatePayload

logger = logging.getLogger("metabase-mcp")


class CardService:
    """Use cases for Metabase cards/questions (`/api/card`)."""

    def __init__(self, gateway: MetabaseGateway) -> None:
        self._gw = gateway

    async def list_cards(self, summary: bool = False) -> Dict[str, Any]:
        result = await self._gw.get("/api/card")
        if not summary:
            return result
        cards = result.get("data", result) if isinstance(result, dict) else result
        trimmed = [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "collection_id": c.get("collection_id"),
                "display": c.get("display"),
                "database": (c.get("dataset_query") or {}).get("database"),
                "type": c.get("type"),
            }
            for c in (cards if isinstance(cards, list) else [])
        ]
        return {"data": trimmed, "count": len(trimmed)}

    async def query_results(self, card_id: int) -> Dict[str, Any]:
        return await self._gw.post(f"/api/card/{card_id}/query")

    async def create(
        self,
        name: str,
        dataset_query: Dict[str, Any],
        display: str,
        type: str = "question",
        visualization_settings: Optional[Union[Dict[str, Any], str]] = None,
        collection_id: Optional[int] = None,
        description: Optional[str] = None,
        parameter_mappings: Optional[List] = None,
        collection_position: Optional[int] = None,
        result_metadata: Optional[List] = None,
        cache_ttl: Optional[int] = None,
        parameters: Optional[List] = None,
        dashboard_id: Optional[int] = None,
        dashboard_tab_id: Optional[int] = None,
        entity_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = CardCreatePayload(
            name=name,
            dataset_query=dataset_query,
            display=display,
            type=type,
            visualization_settings=visualization_settings,
            collection_id=collection_id,
            description=description,
            parameter_mappings=parameter_mappings,
            collection_position=collection_position,
            result_metadata=result_metadata,
            cache_ttl=cache_ttl,
            parameters=parameters,
            dashboard_id=dashboard_id,
            dashboard_tab_id=dashboard_tab_id,
            entity_id=entity_id,
        ).model_dump(exclude_none=True)
        logger.info(f"Creating card '{name}'")
        return await self._gw.post("/api/card", json=payload)

    async def update(
        self,
        card_id: int,
        name: Optional[str] = None,
        dataset_query: Optional[Dict[str, Any]] = None,
        display: Optional[str] = None,
        type: Optional[str] = None,
        visualization_settings: Optional[Union[Dict[str, Any], str]] = None,
        collection_id: Optional[int] = None,
        description: Optional[str] = None,
        parameter_mappings: Optional[List] = None,
        collection_position: Optional[int] = None,
        result_metadata: Optional[List] = None,
        cache_ttl: Optional[int] = None,
        parameters: Optional[List] = None,
        dashboard_id: Optional[int] = None,
        dashboard_tab_id: Optional[int] = None,
        entity_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = CardUpdatePayload(
            name=name,
            dataset_query=dataset_query,
            display=display,
            type=type,
            visualization_settings=visualization_settings,
            collection_id=collection_id,
            description=description,
            parameter_mappings=parameter_mappings,
            collection_position=collection_position,
            result_metadata=result_metadata,
            cache_ttl=cache_ttl,
            parameters=parameters,
            dashboard_id=dashboard_id,
            dashboard_tab_id=dashboard_tab_id,
            entity_id=entity_id,
        ).model_dump(exclude_none=True)
        logger.info(f"Updating card {card_id}")
        return await self._gw.put(f"/api/card/{card_id}", json=payload)

    async def delete(self, card_id: int) -> Dict[str, Any]:
        logger.info(f"Deleting card {card_id}")
        return await self._gw.delete(f"/api/card/{card_id}")

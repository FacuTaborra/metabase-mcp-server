from typing import Any, Dict, Optional

from application.ports.metabase_gateway import MetabaseGateway
from application.schemas import CollectionCreatePayload, CollectionUpdatePayload


class CollectionService:
    """Use cases for Metabase collections (`/api/collection`)."""

    def __init__(self, gateway: MetabaseGateway) -> None:
        self._gw = gateway

    async def list_collections(self, summary: bool = False) -> Dict[str, Any]:
        result = await self._gw.get("/api/collection")
        if not summary:
            return result
        cols = result.get("data", result) if isinstance(result, dict) else result
        trimmed = [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "location": c.get("location"),
                "personal_owner_id": c.get("personal_owner_id"),
            }
            for c in (cols if isinstance(cols, list) else [])
        ]
        return {"data": trimmed, "count": len(trimmed)}

    async def items(self, collection_id: int) -> Dict[str, Any]:
        return await self._gw.get(f"/api/collection/{collection_id}/items")

    async def get(self, collection_id: int) -> Dict[str, Any]:
        return await self._gw.get(f"/api/collection/{collection_id}")

    async def create(
        self,
        name: str,
        color: Optional[str] = None,
        parent_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload = CollectionCreatePayload(
            name=name, color=color, parent_id=parent_id
        ).model_dump(exclude_none=True)
        return await self._gw.post("/api/collection", json=payload)

    async def update(
        self,
        collection_id: int,
        name: Optional[str] = None,
        color: Optional[str] = None,
        parent_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload = CollectionUpdatePayload(
            name=name, color=color, parent_id=parent_id
        ).model_dump(exclude_none=True)
        return await self._gw.put(f"/api/collection/{collection_id}", json=payload)

    async def delete(self, collection_id: int) -> Dict[str, Any]:
        return await self._gw.delete(f"/api/collection/{collection_id}")

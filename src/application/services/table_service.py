import logging
from typing import Any, Dict, Optional

from application.ports.metabase_gateway import MetabaseGateway

logger = logging.getLogger("metabase-mcp")


def _trim_fields(fields: Any) -> list:
    """Reduce a list of Metabase field objects to the keys needed to build MBQL."""
    return [
        {
            "id": f.get("id"),
            "name": f.get("name"),
            "base_type": f.get("base_type"),
            "semantic_type": f.get("semantic_type"),
        }
        for f in (fields or [])
    ]


class TableService:
    """Use cases for Metabase table/database metadata (`/api/database/:id/metadata`,
    `/api/table/:id/query_metadata`).

    These expose the numeric table and field IDs that MBQL queries require, so the
    agent can build a valid `dataset_query` for `create_metabase_card` instead of
    guessing IDs.
    """

    def __init__(self, gateway: MetabaseGateway) -> None:
        self._gw = gateway

    async def get_database_metadata(
        self,
        database_id: int,
        schema: Optional[str] = None,
        summary: bool = True,
    ) -> Dict[str, Any]:
        result = await self._gw.get(f"/api/database/{database_id}/metadata")

        tables = result.get("tables") or []
        if schema is not None:
            tables = [
                t for t in tables if (t.get("schema") or "").lower() == schema.lower()
            ]

        if not summary:
            return {**result, "tables": tables}

        trimmed = [
            {
                "id": t.get("id"),
                "name": t.get("name"),
                "schema": t.get("schema"),
                "display_name": t.get("display_name"),
                "fields": _trim_fields(t.get("fields")),
            }
            for t in tables
        ]
        return {
            "database_id": result.get("id"),
            "name": result.get("name"),
            "tables": trimmed,
            "count": len(trimmed),
        }

    async def get_table_metadata(
        self,
        table_id: int,
        summary: bool = True,
    ) -> Dict[str, Any]:
        result = await self._gw.get(f"/api/table/{table_id}/query_metadata")

        if not summary:
            return result

        return {
            "id": result.get("id"),
            "name": result.get("name"),
            "schema": result.get("schema"),
            "display_name": result.get("display_name"),
            "db_id": result.get("db_id"),
            "fields": _trim_fields(result.get("fields")),
        }

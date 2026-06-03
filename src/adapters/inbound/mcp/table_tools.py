from typing import Any, Dict, Optional

from fastmcp import FastMCP

from application.services import TableService


def register_table_tools(mcp: FastMCP, service: TableService) -> None:
    @mcp.tool()
    async def get_metabase_database_metadata(
        database_id: int,
        schema: Optional[str] = None,
        summary: bool = True,
    ) -> Dict[str, Any]:
        """
        Get the tables and fields of a database, with the numeric IDs needed to build MBQL.

        Use this to discover the IDs required for a structured (MBQL) `dataset_query`
        before calling `create_metabase_card`:
          - a table's `id` -> the MBQL `"source-table"` value.
          - a field's `id` -> field references `["field", <id>, null]` used in
            `aggregation`, `breakout` and `filter`.

        Args:
            database_id (int): ID of the database (see `get_metabase_databases`).
            schema (str, optional): If given, return only tables in this schema
                (case-insensitive). Use it to focus on one schema (e.g. "tms") in a
                database that has many.
            summary (bool, optional): If True (default), return a trimmed shape
                {database_id, name, tables:[{id, name, schema, display_name,
                fields:[{id, name, base_type, semantic_type}]}]} to avoid huge
                payloads. Set False to get the full Metabase metadata object.

        Returns:
            Dict[str, Any]: Tables (with ids) and their fields (with ids and types).
        """
        return await service.get_database_metadata(
            database_id=database_id, schema=schema, summary=summary
        )

    @mcp.tool()
    async def get_metabase_table_metadata(
        table_id: int,
        summary: bool = True,
    ) -> Dict[str, Any]:
        """
        Get the fields of a single table, with the numeric IDs needed to build MBQL.

        Lighter than `get_metabase_database_metadata` when you already know the
        `table_id`. Use a field's `id` in MBQL field references `["field", <id>, null]`,
        and the table `id` as the `"source-table"` value, when building a
        `dataset_query` for `create_metabase_card`.

        Args:
            table_id (int): ID of the table.
            summary (bool, optional): If True (default), return a trimmed shape
                {id, name, schema, display_name, db_id, fields:[{id, name, base_type,
                semantic_type}]}. Set False to get the full query_metadata object.

        Returns:
            Dict[str, Any]: The table identity and its fields (with ids and types).
        """
        return await service.get_table_metadata(table_id=table_id, summary=summary)

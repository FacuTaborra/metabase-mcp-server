from typing import Any, Dict, List, Optional, Union

from fastmcp import FastMCP

from application.services import CardService


def register_card_tools(mcp: FastMCP, service: CardService) -> None:
    @mcp.tool()
    async def get_metabase_cards(summary: bool = False) -> Dict[str, Any]:
        """
        Get a list of all saved questions (cards).

        Args:
            summary (bool, optional): If True, return only {id, name, collection_id,
                display, database, type} per card instead of the full objects
                (avoids huge result_metadata / dataset_query payloads). Default False.

        Returns:
            Dict[str, Any]: Cards metadata including names, ids, collections.
        """
        return await service.list_cards(summary=summary)

    @mcp.tool()
    async def get_card_query_results(card_id: int) -> Dict[str, Any]:
        """
        Get the results of a card's query.

        Args:
            card_id (int): ID of the card.

        Returns:
            Dict[str, Any]: Query result data.
        """
        return await service.query_results(card_id)

    @mcp.tool()
    async def create_metabase_card(
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
        entity_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new card (chart/table) via POST /api/card, using SQL or MBQL.

        Args:
            name: Display name of the card.
            dataset_query: The query. Native SQL:
                {"type": "native", "native": {"query": "SELECT ..."}, "database": <id>}.
                For `{{variable}}` placeholders add "template-tags": {...} inside "native".
                MBQL: {"type": "query", "query": {...}, "database": <id>}.
            display: Visualization type — "table", "bar", "line", "pie", "area",
                "scatter", "funnel", "pivot-table", "map", "scalar", etc.
            type: Card type — "question" (default), "metric" or "model".
            visualization_settings: Per-chart formatting; shape varies by `display`
                (e.g. {"graph": {...}} for bar/line, {"pie": {...}} for pie). Optional.
            collection_id: Collection to save into.
            description: Help text for the card.
            parameter_mappings: Mappings linking dashboard filters to this card.
            collection_position, result_metadata, cache_ttl, parameters, dashboard_id,
            dashboard_tab_id, entity_id: Optional passthrough fields.

        Returns:
            Dict[str, Any]: The created card (id, name, dataset_query, ...).

        Example:
            >>> await create_metabase_card(
                    name="Seats by destination", display="bar",
                    dataset_query={"type": "native",
                        "native": {"query": "SELECT destination, COUNT(*) FROM flights GROUP BY 1"},
                        "database": 2},
                    collection_id=3)
        """
        return await service.create(
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
        )

    @mcp.tool()
    async def update_metabase_card(
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
        entity_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing card in Metabase.

        Args:
            card_id (int): ID of the card to update.
            name (str, optional): New name of the card.
            dataset_query (Dict[str, Any], optional): Dataset query definition.
            display (str, optional): Display type.
            type (str, optional): Card type.
            visualization_settings (Dict[str, Any], optional): Visualization settings.
            collection_id (int, optional): ID of the collection.
            description (str, optional): Description of the card.
            parameter_mappings (list, optional): Parameter mappings.
            collection_position (int, optional): Position in the collection.
            result_metadata (list, optional): Metadata for results.
            cache_ttl (int, optional): Cache TTL.
            parameters (list, optional): Query parameters.
            dashboard_id (int, optional): Dashboard ID.
            dashboard_tab_id (int, optional): Dashboard tab ID.
            entity_id (str, optional): Entity ID.

        Returns:
            Dict[str, Any]: Updated card metadata.
        """
        return await service.update(
            card_id=card_id,
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
        )

    @mcp.tool()
    async def delete_metabase_card(card_id: int) -> Dict[str, Any]:
        """
        Delete a card from Metabase.

        Args:
            card_id (int): ID of the card to delete.

        Returns:
            Dict[str, Any]: Deletion confirmation.
        """
        return await service.delete(card_id)

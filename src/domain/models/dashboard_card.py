from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_serializer


class DashboardCard(BaseModel):
    """
    Represents a card within a Metabase dashboard.

    This shape mirrors each object in the `dashcards` array that
    `GET /api/dashboard/:id` returns and `PUT /api/dashboard/:id` expects.

    Attributes:
        id: Use negative numbers so Metabase auto-assigns the real id.
        row: Row position in the dashboard grid.
        col: Column position in the dashboard grid.
        size_x: Width in grid units.
        size_y: Height in grid units.
        card_id: ID of the card/visualization. None for virtual cards
            (heading/text/link/iframe), whose content lives in visualization_settings.
        parameter_mappings: Parameter mappings for the card.
        series: Additional cards for combined/multi-series visualizations.
        visualization_settings: Per-dashcard visualization overrides.
        dashboard_tab_id: Tab this card belongs to. None when the dashboard has no tabs.
        inline_parameters: IDs of dashboard parameters rendered inline on this card.
    """

    id: int
    row: int
    col: int
    size_x: int
    size_y: int
    card_id: Optional[int] = None
    parameter_mappings: List[Dict[str, Any]] = Field(default_factory=list)
    series: List[Dict[str, Any]] = Field(default_factory=list)
    visualization_settings: Dict[str, Any] = Field(default_factory=dict)
    dashboard_tab_id: Optional[int] = None
    inline_parameters: Optional[List[str]] = None

    @model_serializer(mode="plain")
    def serialize(self) -> Dict[str, Any]:
        """Serialize for the Metabase API.

        card_id is always included even when None (virtual cards legitimately have
        card_id=null). dashboard_tab_id and inline_parameters are omitted when None
        rather than sent as null.
        """
        data: Dict[str, Any] = {
            "id": self.id,
            "row": self.row,
            "col": self.col,
            "size_x": self.size_x,
            "size_y": self.size_y,
            "card_id": self.card_id,
            "parameter_mappings": self.parameter_mappings,
            "series": self.series,
            "visualization_settings": self.visualization_settings,
        }
        if self.dashboard_tab_id is not None:
            data["dashboard_tab_id"] = self.dashboard_tab_id
        if self.inline_parameters is not None:
            data["inline_parameters"] = self.inline_parameters
        return data

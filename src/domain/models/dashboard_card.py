from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DashboardCard:
    """
    Represents a card within a Metabase dashboard.

    This shape mirrors each object in the `dashcards` array that
    `GET /api/dashboard/:id` returns and `PUT /api/dashboard/:id` expects.

    Attributes:
        id (int): Use negative numbers to auto generate the ids
            or use any unique value but,
            it must be unique within the dashboard
        row (int): The row position in the dashboard grid
        col (int): The column position in the dashboard grid
        size_x (int): The width of the card in grid units
        size_y (int): The height of the card in grid units
        card_id (Optional[int]): The ID of the card/visualization. Leave None for
            "virtual" cards (heading / text / link / iframe), whose content lives in
            visualization_settings (e.g. {"virtual_card": {...}, "text": "..."}).
        parameter_mappings (List[Dict[str, Any]]): Parameter mappings for the card
        series (List[Dict[str, Any]]): Additional cards for combined/multi-series
            visualizations. Empty for a single-card dashcard.
        visualization_settings (Dict[str, Any]): Per-dashcard visualization overrides
            (formatting, axes, etc.) applied on top of the saved card.
        dashboard_tab_id (Optional[int]): ID of the dashboard tab this card belongs to.
            Leave None when the dashboard has no tabs.
        inline_parameters (Optional[List[str]]): IDs of dashboard parameters rendered
            inline on this card (newer Metabase feature). None when unused.
    """
    id: int  # Use negative numbers to auto generate the ids
    row: int
    col: int
    size_x: int
    size_y: int
    card_id: Optional[int] = None  # None for virtual cards (heading/text/link/iframe)
    parameter_mappings: List[Dict[str, Any]] = field(default_factory=list)
    series: List[Dict[str, Any]] = field(default_factory=list)
    visualization_settings: Dict[str, Any] = field(default_factory=dict)
    dashboard_tab_id: Optional[int] = None
    inline_parameters: Optional[List[str]] = None

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from domain.models import DashboardCard, DashboardTab, EmbeddingParams


class DashboardCreatePayload(BaseModel):
    name: str
    description: Optional[str] = None
    collection_id: Optional[int] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    tabs: Optional[List[DashboardTab]] = None
    cache_ttl: Optional[int] = None
    collection_position: Optional[int] = None


class DashboardUpdatePayload(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    collection_id: Optional[int] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    tabs: Optional[List[DashboardTab]] = None
    dashcards: Optional[List[DashboardCard]] = None
    points_of_interest: Optional[str] = None
    caveats: Optional[str] = None
    enable_embedding: Optional[bool] = None
    embedding_params: Optional[EmbeddingParams] = None
    archived: Optional[bool] = None
    position: Optional[int] = None
    collection_position: Optional[int] = None
    cache_ttl: Optional[int] = None
    width: Optional[str] = None
    show_in_getting_started: Optional[bool] = None

    @field_validator("width")
    @classmethod
    def validate_width(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("fixed", "full"):
            raise ValueError("width must be either 'fixed' or 'full'")
        return v


class DashboardCopyPayload(BaseModel):
    name: str
    description: Optional[str] = None
    collection_id: Optional[int] = None
    is_deep_copy: bool = False
    collection_position: Optional[int] = None


class DashboardAddCardPayload(BaseModel):
    id: int = -1
    card_id: int
    row: int
    col: int
    size_x: int
    size_y: int
    series: List[Dict[str, Any]] = Field(default_factory=list)
    parameter_mappings: List[Dict[str, Any]] = Field(default_factory=list)
    visualization_settings: Dict[str, Any] = Field(default_factory=dict)
    dashboard_tab_id: Optional[int] = None

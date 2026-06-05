import json
import logging
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger("metabase-mcp")


def _normalize_visualization_settings(v: Union[Dict[str, Any], str, None]) -> Dict[str, Any]:
    if v is None:
        return {}
    if isinstance(v, str):
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in visualization_settings")
            raise ValueError("visualization_settings must be a valid JSON object")
    return v


class CardCreatePayload(BaseModel):
    name: str
    dataset_query: Dict[str, Any]
    display: str
    type: str = "question"
    visualization_settings: Dict[str, Any] = Field(default_factory=dict)
    collection_id: Optional[int] = None
    description: Optional[str] = None
    parameter_mappings: Optional[List] = None
    collection_position: Optional[int] = None
    result_metadata: Optional[List] = None
    cache_ttl: Optional[int] = None
    parameters: Optional[List] = None
    dashboard_id: Optional[int] = None
    dashboard_tab_id: Optional[int] = None
    entity_id: Optional[str] = None

    @field_validator("visualization_settings", mode="before")
    @classmethod
    def normalize_viz(cls, v: Any) -> Dict[str, Any]:
        return _normalize_visualization_settings(v)


class CardUpdatePayload(BaseModel):
    name: Optional[str] = None
    dataset_query: Optional[Dict[str, Any]] = None
    display: Optional[str] = None
    type: Optional[str] = None
    visualization_settings: Dict[str, Any] = Field(default_factory=dict)
    collection_id: Optional[int] = None
    description: Optional[str] = None
    parameter_mappings: Optional[List] = None
    collection_position: Optional[int] = None
    result_metadata: Optional[List] = None
    cache_ttl: Optional[int] = None
    parameters: Optional[List] = None
    dashboard_id: Optional[int] = None
    dashboard_tab_id: Optional[int] = None
    entity_id: Optional[str] = None

    @field_validator("visualization_settings", mode="before")
    @classmethod
    def normalize_viz(cls, v: Any) -> Dict[str, Any]:
        return _normalize_visualization_settings(v)

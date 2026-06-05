from typing import Any, Dict, Optional

from pydantic import BaseModel


class DatabaseCreatePayload(BaseModel):
    name: str
    engine: str
    details: Dict[str, Any]
    auto_run_queries: Optional[bool] = None
    cache_ttl: Optional[int] = None
    is_full_sync: Optional[bool] = None
    schedule: Optional[Dict[str, Any]] = None
    timezone: Optional[str] = None
    metadata_sync: Optional[bool] = None


class DatabaseUpdatePayload(BaseModel):
    name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    auto_run_queries: Optional[bool] = None
    cache_ttl: Optional[int] = None
    is_full_sync: Optional[bool] = None
    schedule: Optional[Dict[str, Any]] = None
    timezone: Optional[str] = None
    metadata_sync: Optional[bool] = None

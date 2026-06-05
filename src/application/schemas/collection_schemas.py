from typing import Optional

from pydantic import BaseModel


class CollectionCreatePayload(BaseModel):
    name: str
    color: Optional[str] = None
    parent_id: Optional[int] = None


class CollectionUpdatePayload(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    parent_id: Optional[int] = None

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class UserCreatePayload(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    login_attributes: Optional[Dict[str, Any]] = None
    group_ids: Optional[List] = None
    is_superuser: Optional[bool] = None


class UserUpdatePayload(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    login_attributes: Optional[Dict[str, Any]] = None
    group_ids: Optional[List] = None
    is_superuser: Optional[bool] = None

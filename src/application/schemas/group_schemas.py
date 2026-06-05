from typing import Optional

from pydantic import BaseModel


class GroupCreatePayload(BaseModel):
    name: str
    ldap_dn: Optional[str] = None

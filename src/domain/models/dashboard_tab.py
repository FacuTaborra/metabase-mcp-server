from typing import Optional

from pydantic import BaseModel


class DashboardTab(BaseModel):
    """Represents a tab within a Metabase dashboard."""

    id: Optional[int] = None
    name: str = ""

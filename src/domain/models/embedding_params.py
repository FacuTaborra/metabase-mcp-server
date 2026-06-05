from typing import Optional

from pydantic import BaseModel


class EmbeddingParams(BaseModel):
    """Represents embedding parameters for Metabase dashboards."""

    url: Optional[str] = None
    custom_css: Optional[str] = None

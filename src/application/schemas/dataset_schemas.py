from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class NativeQueryPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    query: str
    template_tags: Optional[Dict[str, Any]] = Field(None, alias="template-tags")

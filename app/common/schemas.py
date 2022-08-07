from __future__ import annotations

from pydantic import BaseModel


###
# Common Utilities Models
###
class SimpleMessageResponse(BaseModel):
    message: str

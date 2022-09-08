from __future__ import annotations

from pydantic import BaseModel


class Wallet(BaseModel):
    id: int
    address: str
    address_type: str
    user_id: int | None

    class Config:
        orm_mode = True

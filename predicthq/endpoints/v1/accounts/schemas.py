from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Industry(BaseModel):
    id: str
    name: str


class Account(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    industry: Optional[Industry] = None
    created_at: datetime
    updated_at: datetime

from datetime import datetime

from pydantic import BaseModel


class Industry(BaseModel):
    id: str
    name: str


class Account(BaseModel):
    id: str
    name: str
    description: str
    industry: Industry
    created_at: datetime
    updated_at: datetime

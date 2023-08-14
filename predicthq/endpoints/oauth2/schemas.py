from typing import List, Optional, Union

from pydantic import BaseModel, field_validator

from predicthq.config import config


class AccessToken(BaseModel):
    access_token: str
    token_type: str
    scope: List[str]
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

    @field_validator("scope", mode="before")
    def parse_scope(cls, value: Optional[Union[List[str], str]] = None):
        if isinstance(value, str):
            if " " in value:
                return value.split(" ")
            elif "," in value:
                return value.split(",")
            return [value]
        return value

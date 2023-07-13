from predicthq.config import config
from predicthq.endpoints.schemas import (
    ConfigMixin,
    IntType,
    Model,
    StringType,
    StringListType,
)

class AccessToken(Model):
    access_token = StringType()
    token_type = StringType()
    scope = StringListType(StringType, separator=" ")
    refresh_token = StringType(serialize_when_none=False)
    expires_in = IntType(serialize_when_none=False)

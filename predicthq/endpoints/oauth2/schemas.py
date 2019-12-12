from predicthq.config import config
from predicthq.endpoints.schemas import Model, StringType, StringListType, IntType


class GetTokenParams(Model):

    class Options:
        serialize_when_none = False

    client_id = StringType(default=lambda: config.OAUTH2_CLIENT_ID, required=True)
    client_secret = StringType(default=lambda: config.OAUTH2_CLIENT_SECRET, required=True)
    scope = StringListType(StringType, default=lambda: config.OAUTH2_SCOPE, separator=" ")
    grant_type = StringType(choices=('client_credentials',), default='client_credentials', required=True)


class RevokeTokenParams(Model):

    class Options:
        serialize_when_none = False

    client_id = StringType(default=lambda: config.OAUTH2_CLIENT_ID, required=True)
    client_secret = StringType(default=lambda: config.OAUTH2_CLIENT_SECRET, required=True)
    token = StringType(required=True)
    token_type_hint = StringType(choices=('access_token', 'refresh_token'), default='access_token', required=True)


class AccessToken(Model):

    access_token = StringType()
    token_type = StringType()
    scope = StringListType(StringType, separator=" ")
    refresh_token = StringType(serialize_when_none=False)
    expires_in = IntType(serialize_when_none=False)

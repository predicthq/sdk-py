from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .decorators import preload_config_defaults
from .schemas import AccessToken


class OAuth2Endpoint(BaseEndpoint):
    @accepts()
    @preload_config_defaults(["client_id", "client_secret", "scope", "grant_type"])
    @returns(AccessToken)
    def get_token(self, client_id, client_secret, scope, grant_type, **kwargs):
        verify_ssl = kwargs.pop("config.verify_ssl", True)
        data = {
            "grant_type": grant_type,
            "scope": scope,
        }
        data.update(kwargs)
        return self.client.post(
            "/oauth2/token/",
            auth=(client_id, client_secret),
            data=data,
            verify=verify_ssl,
        )

    @accepts()
    @preload_config_defaults(["client_id", "client_secret", "token_type_hint"])
    def revoke_token(self, client_id, client_secret, token, token_type_hint, **kwargs):
        verify_ssl = kwargs.pop("config.verify_ssl", True)
        data = {
            "token_type_hint": token_type_hint,
            "token": token,
        }
        self.client.post(
            "/oauth2/revoke/",
            auth=(client_id, client_secret),
            data=data,
            verify=verify_ssl,
        )

from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import returns
from .schemas import Account
from deprecated import deprecated


class AccountsEndpoint(BaseEndpoint):
    @deprecated(
        reason=(
            "The Accounts endpoint in the SDK is deprecated and will be removed in future releases. "
            "Account information can be managed via the PredictHQ dashboard."
        ),
        category=FutureWarning,
    )
    @returns(Account)
    def self(self):
        return self.client.get(self.build_url("v1", "accounts/self"))

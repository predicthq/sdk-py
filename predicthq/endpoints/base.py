class MetaEndpoint(type):

    def __new__(mcs, name, bases, data):
        if 'Meta' not in data:
            class Meta:
                """ Used by decorators when overriding schema classes """
                pass
            data['Meta'] = Meta
        return super(MetaEndpoint, mcs).__new__(mcs, name, bases, data)


class BaseEndpoint(metaclass=MetaEndpoint):

    def __init__(self, client):
        self.client = client

    def build_url(self, prefix, suffix):
        return '/{}/{}/'.format(prefix.strip('/'), suffix.strip('/'))


class UserBaseEndpoint(BaseEndpoint):

    def __init__(self, client, account_id=None):
        self.account_id = account_id
        super(UserBaseEndpoint, self).__init__(client)

    def for_account(self, account_id):
        """
        Parameterised endpoint for account.

        Required when using a user access token, as the user may belong to multiple accounts with different plans

        """
        return self.__class__(self.client, account_id)

    def build_url(self, prefix, suffix):
        if self.account_id is not None:
            return '/{}/accounts/{}/{}/'.format(prefix.strip('/'), self.account_id, suffix.strip('/'))
        else:
            return super(UserBaseEndpoint, self).build_url(prefix, suffix)

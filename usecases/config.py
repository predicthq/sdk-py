from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# You can modify some of the underlying behaviour of the HTTP library with
# the `config` parameter.

# As an example, you can disable SSL verification as follows
for event in phq.events.search(config__verify_ssl=False):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))

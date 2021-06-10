from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# broadcasts and events endpoints use the same approach for search pagination.
# The following examples are on the events endpoint but you can reuse them
# for the broadcasts endpoint.


# By default the search() method only returns the first
# page of results, with a default page size of 10.
# It's because the default values for the offset and limit parameters
# are respectively 0 and 10.
for event in phq.events.search():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))


# You can modify this behaviour by specifying an offset and/or a limit.
# The following example skips the first 10 results (offset=10)
# and limits the results to 5 items (limit=5).
for event in phq.events.search(offset=10, limit=5):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))


# You can then iterate over the search results set by continuously
# incrementing the offset by the limit value step.
search_params = {
    'category': 'sports',
    'start': {'gte': '2018-05-01', 'lte': '2018-06-30'},
    'within': '10km@-36.844480,174.768368'
}

results_count = phq.events.count(**search_params).count
print(f'Results count: {results_count}')

search_params_with_offset_limit = {**search_params, **{'offset': '0', 'limit': '10'}}

for offset in range(0, results_count, 10):
    for event in phq.events.search(**search_params_with_offset_limit):
        print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))


# The Python SDK provides helpers for iterating over the results pages.
# You can chain the iter_all() generator to iterate over all your results.
for event in phq.events.search(**search_params).iter_all():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))


# There is a maximum number of results returned by a single search query
# (currently set at 100k results). Paginating won't allow you to go beyond
# this limit.
# The overflow field will inform on you whether you are above this limit or not.
# If that's the case, you need to refine your query to get a smaller set of results
# (e.g. add a `start` or `updated` parameter, add a `category`, etc.).
# If you are likely to get above this limit, it's a good idea to add a test
# and potentially raise in your code.
event_result_set_without_filters = phq.events.search()
if event_result_set_without_filters.overflow is True:
    raise RuntimeError("Result set overflowed")

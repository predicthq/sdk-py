# PredictHQ API Client for Python

[![Version](https://badge.fury.io/gh/predicthq%2Fsdk-py.svg)](https://badge.fury.io/gh/predicthq%2Fsdk-py)
[![PyPI package](https://badge.fury.io/py/predicthq.svg)](https://badge.fury.io/py/predicthq)
[![Build Status](https://travis-ci.org/predicthq/sdk-py.svg?branch=master)](https://travis-ci.org/predicthq/sdk-py)
[![Coverage Status](https://coveralls.io/repos/github/predicthq/sdk-py/badge.svg?branch=master)](https://coveralls.io/github/predicthq/sdk-py?branch=master)


[PredictHQ](https://www.predicthq.com/) is the demand intelligence company combining real-world events into one global source of truth to help businesses better understand demand and plan for the future.

## Installation

```Shell
pip install predicthq
```

## Usage

### Events endpoint

Additional examples are available in [usecases/events](usecases/events) directory.

```Python
from predicthq import Client

phq = Client(access_token="$ACCESS_TOKEN")

# the search() method returns an EventResultSet which allows you to iterate over the 1st page of items
for event in phq.events.search(q="Foo Fighters", rank_level=[4, 5], place={"scope": ["5391959", "5368361"]}):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))

# if you want to iterate over all the results for your query, you can chain the iter_all() generator
for event in phq.events.search(q="matisse", country="FR").iter_all():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))

# you can skip results with the offset parameter and limit the number of results with the limit parameter
# the following skips the first 10 results and limits the results to 5 items
for event in phq.events.search(q="matisse", country="FR", offset=10, limit=5):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
```

## Endpoints

* `Client.oauth2`
* `Client.accounts`
* `Client.events`
* `Client.signals`
* `Client.places`

For a description of all available endpoints, refer to our [API Documentation](https://developer.predicthq.com/).

## Running Tests

```Shell
pip install tox
tox
```

## Found a Bug?

Please [log an issue](https://github.com/predicthq/sdk-py/issues/new>).

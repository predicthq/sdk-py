<p align="center"><img src="ext/logo.png" alt="PredictHQ logo"></p>

# PredictHQ API Client for Python

[![Version](https://badge.fury.io/gh/predicthq%2Fsdk-py.svg)](https://badge.fury.io/gh/predicthq%2Fsdk-py)
[![PyPI package](https://badge.fury.io/py/predicthq.svg)](https://badge.fury.io/py/predicthq)
[![Build Status](https://travis-ci.org/predicthq/sdk-py.svg?branch=master)](https://travis-ci.org/predicthq/sdk-py)
[![Coverage Status](https://coveralls.io/repos/github/predicthq/sdk-py/badge.svg?branch=master)](https://coveralls.io/github/predicthq/sdk-py?branch=master)


[PredictHQ](https://www.predicthq.com/) is the demand intelligence company combining real-world events into one global source of truth to help businesses better understand demand and plan for the future.

## Installation

The PredictHQ Python client is distributed as a pip package. You can simply install it by running

```Shell
pip install predicthq
```

## Usage

We support all the endpoints available in our API.

* `oauth2`
* `accounts`
* `events`
* `places`

Please refer to our [API Documentation](https://docs.predicthq.com/) for a description of each endpoint.

### Pagination

Additional examples are available in [usecases/pagination.py](https://github.com/predicthq/sdk-py/tree/master/usecases/pagination.py) file.

By default the `search()` method only returns the first page of results, with a default page size of 10.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for event in phq.events.search():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
```

You can chain the `iter_all()` generator to iterate over *all* your events.

```Python
for event in phq.events.search().iter_all():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
```

### Events endpoint

Additional examples are available in [usecases/events](https://github.com/predicthq/sdk-py/tree/master/usecases/events) folder.

The following example searches for the 'Katy Perry' events (full text search) with rank level of 4 or 5 (rank >= 60) in the concerts category.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for event in phq.events.search(q='Katy Perry', rank_level=[4, 5], category='concerts'):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
```

Please refer to our [Events endpoint documentation](https://docs.predicthq.com/resources/events/) for the lists of search parameters and event fields available.

### Places endpoint

Additional examples are available in [usecases/places.py](https://github.com/predicthq/sdk-py/tree/master/usecases/places.py) file.

The following example searches for the 'New York' places (full text search) in the US.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for place in phq.places.search(q='New York', country='US'):
    print(place.id, place.name, place.type, place.location)
```

Please refer to our [Places endpoint documentation](https://docs.predicthq.com/resources/places/) for the lists of search parameters and place fields available.

## Running Tests

```Shell
pip install tox
tox
```

## Found a Bug?

Please [log an issue](https://github.com/predicthq/sdk-py/issues/new).

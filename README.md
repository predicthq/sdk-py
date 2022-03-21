<p align="center"><img src="ext/logo.png" alt="PredictHQ logo"></p>

# PredictHQ API Client for Python

[![Version](https://badge.fury.io/gh/predicthq%2Fsdk-py.svg)](https://badge.fury.io/gh/predicthq%2Fsdk-py)
![build](https://github.com/predicthq/sdk-py/actions/workflows/publish-to-test-pypi.yml/badge.svg)
[![PyPI package](https://badge.fury.io/py/predicthq.svg)](https://badge.fury.io/py/predicthq)


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
* `broadcasts`
* `events`
* `features`
* `places`

Please refer to our [API Documentation](https://docs.predicthq.com/) for a description of each endpoint.

The [usecases/](https://github.com/predicthq/sdk-py/tree/master/usecases/pagination.py) folder is a good starting point to get familiar with the Python SDK.
You can also review the [tests](https://github.com/predicthq/sdk-py/tree/master/tests/endpoints/v1/) for a kitchen sink of all the parameters available per endpoint.

### Pagination

Additional examples are available in [usecases/pagination.py](https://github.com/predicthq/sdk-py/tree/master/usecases/pagination.py) file.

By default the `search()` method only returns the first page of results, with a default page size of 10.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for event in phq.events.search():
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))
```

You can chain the `iter_all()` generator to iterate over *all* your events.

```Python
for event in phq.events.search().iter_all():
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))
```

### Events endpoint

Additional examples are available in [usecases/events](https://github.com/predicthq/sdk-py/tree/master/usecases/events) folder.

The following example searches for the 'Katy Perry' events (full text search) with rank level of 4 or 5 (rank >= 60) in the concerts category.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for event in phq.events.search(q='Katy Perry', rank_level=[4, 5], category='concerts'):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))
```

Please refer to our [Events endpoint documentation](https://docs.predicthq.com/resources/events/) for the lists of search parameters and event fields available.

### Broadcasts endpoint

Additional examples are available in [usecases/broadcasts](https://github.com/predicthq/sdk-py/tree/master/usecases/broadcasts) folder.

The following example searches for the broadcasts with PHQ viewership gte 100 and with event (the physical event the broadcast links to) label 'nfl'.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for broadcast in phq.broadcasts.search(phq_viewership__gte=100, event__label='nfl'):
    print(broadcast.event.title, broadcast.phq_viewership, broadcast.event.labels, broadcast.dates.start.strftime("%Y-%m-%d"))
```

Please refer to our [Broadcasts endpoint documentation](https://docs.predicthq.com/resources/broadcasts/) for the lists of search parameters and broadcast fields available.

### Places endpoint

Additional examples are available in [usecases/places.py](https://github.com/predicthq/sdk-py/tree/master/usecases/places.py) file.

The following example searches for the 'New York' places (full text search) in the US.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for place in phq.places.search(q="New York", country="US"):
    print(place.id, place.name, place.type, place.location)
```

Please refer to our [Places endpoint documentation](https://docs.predicthq.com/resources/places/) for the lists of search parameters and place fields available.

### Features endpoint

The following example obtain features of events which are active between 2017-12-31 and 2018-01-02, with place_id 4671654. 

Requested features:
* rank_levels for public_holidays
* count and median of sporting events which has a phq_rank greater than 50

By place_id list (e.g. Austin):
```Python
from predicthq import Client

phq = Client(access_token="abc123")


for feature in phq.features.obtain_features(
        active__gte="2017-12-31",
        active__lte="2018-01-02",
        location__place_id=[4671654],
        phq_rank_public_holidays=True,
        phq_attendance_sports__stats=["count", "median"],
        phq_attendance_sports__phq_rank={
            "gt": 50
        }
):
    print(feature.date, feature.phq_attendance_sports.stats.count, feature.phq_rank_public_holidays.rank_levels)
```
by geo:
```Python
from predicthq import Client

phq = Client(access_token="abc123")


for feature in phq.features.obtain_features(
        active__gte="2017-12-31",
        active__lte="2018-01-02",
        location__geo={
            "lon": -97.74306,
            "lat": 30.26715,
            "radius": "150km"
        },
        phq_rank_public_holidays=True,
        phq_attendance_sports__stats=["count", "median"],
        phq_attendance_sports__phq_rank={
            "gt": 50
        }
):
    print(feature.date, feature.phq_attendance_sports.stats.count, feature.phq_rank_public_holidays.rank_levels)
```

The following example obtains features of broadcasts which are active between 2017-12-31 and 2018-01-02, with place_id 4671654

Requested features:
* count and median of broadcasts which start between 9am - 11am and have a `phq_rank` greater than 50

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for feature in phq.features.obtain_features(
        active__gte="2017-12-31",
        active__lte="2018-01-02",
        hour_of_day_start__gt=9,
        hour_of_day_start__lte=11,
        location__place_id=[4671654],
        phq_viewership_sports_american_football__stats=["count", "median"],
        phq_viewership_sports_american_football__phq_rank={
            "gt": 50
        }
):
    print(feature.date, feature.phq_viewership_sports_american_football.stats.count, feature.phq_viewership_sports_american_football.stats.median)
```

Please refer to our [Features endpoint documentation](https://docs.predicthq.com/start/features-api/) for the lists of supported features and response fields available.

### Config parameters

We support some `config` parameters for additional flexibility.

Supported config parameters:
- `verify_ssl`

```Python
from predicthq import Client

phq = Client(access_token="abc123")


# double underscore syntax
for event in phq.events.search(config__verify_ssl=False):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))

# dictionary syntax
for event in phq.events.search(config={"verify_ssl": False}):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))
```


## Running Tests

```Shell
pip install tox
tox
```

## Found a Bug?

Please [log an issue](https://github.com/predicthq/sdk-py/issues/new).

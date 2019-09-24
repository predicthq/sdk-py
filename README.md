<img align="center" src="ext/logo.png" alt="PredictHQ logo">

# PredictHQ API Client for Python

[![Version](https://badge.fury.io/gh/predicthq%2Fsdk-py.svg)](https://badge.fury.io/gh/predicthq%2Fsdk-py)
[![PyPI package](https://badge.fury.io/py/predicthq.svg)](https://badge.fury.io/py/predicthq)
[![Build Status](https://travis-ci.org/predicthq/sdk-py.svg?branch=master)](https://travis-ci.org/predicthq/sdk-py)
[![Coverage Status](https://coveralls.io/repos/github/predicthq/sdk-py/badge.svg?branch=master)](https://coveralls.io/github/predicthq/sdk-py?branch=master)


[PredictHQ](https://www.predicthq.com/) is the demand intelligence company combining real-world events into one global source of truth to help businesses better understand demand and plan for the future.

## Installation

The PredicHQ Python client is distributed as a pip package. You can simply install it by running

```Shell
pip install predicthq
```

## Usage

We support all the endpoints available in our API.

* `oauth2`
* `accounts`
* `events`
* `places`

Please refer to our [API Documentation](https://developer.predicthq.com/) for a description of each endpoint.

### Pagination

Additional examples are available in [usecases/pagination.py](usecases/pagination.py) file.

By default the `search()` method only returns the first page of results, with a default page size of 10.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for event in phq.events.search():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
```

```
51 performing-arts Emociones Encontradas 2039-12-31
0 concerts Sister Hazel 2039-01-02
0 concerts Tommy Lee 2039-01-02
70 concerts BE-BOP AUTUMN JAZZ TOUR 2039-01-02
87 concerts Nsync 2039-01-02
56 performing-arts RAGTIME 2039-01-02
48 concerts Styx 2039-01-02
75 concerts Jimmy Page & the Black Crowes Live 2039-01-02
76 concerts Aerosmith 2039-01-02
72 concerts AVALON ANOINTED WITH GUEST NICHOLE NORDEMAN 2039-01-02
```

You can chain the `iter_all()` generator to iterate over *all* your events.

```Python
for event in phq.events.search().iter_all():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
```

```
51 performing-arts Emociones Encontradas 2039-12-31
0 concerts Sister Hazel 2039-01-02
0 concerts Tommy Lee 2039-01-02
70 concerts BE-BOP AUTUMN JAZZ TOUR 2039-01-02
87 concerts Nsync 2039-01-02
56 performing-arts RAGTIME 2039-01-02
48 concerts Styx 2039-01-02
75 concerts Jimmy Page & the Black Crowes Live 2039-01-02
76 concerts Aerosmith 2039-01-02
72 concerts AVALON ANOINTED WITH GUEST NICHOLE NORDEMAN 2039-01-02
76 concerts MERRY MAYHEM TOUR : OZZY OSBOURNE AND ROB ZOMBIE 2039-01-02
70 concerts Mormon Tabernacle Choir 2039-01-01
0 concerts THE ANNUAL LEGEND'S OF RASTA REGGAE FESTIVAL 2039-01-01
...
```

### Events endpoint

Additional examples are available in [usecases/events.py](usecases/events.py) file.

The following example searches for the 'Katy Perry' events (full text search) with rank level of 4 or 5 (rank >= 60) in the concerts category.

```Python
from predicthq import Client

phq = Client(access_token="abc123")


for event in phq.events.search(q='Katy Perry', rank_level=[4, 5], category='concerts'):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
```

```
76 concerts KATY PERRY 2011-11-22
70 concerts Katy Perry 2011-06-09
77 concerts Katy Perry 2014-08-11
73 concerts Katy Perry 2011-08-10
76 concerts Katy Perry 2014-08-23
72 concerts Katy Perry 2018-04-08
75 concerts Katy Perry 2015-10-13
76 concerts Katy Perry 2014-12-12
74 concerts Katy Perry 2014-12-10
74 concerts Katy Perry 2014-11-18
```

Please refer to our [Events endpoint documentation](https://developer.predicthq.com/resources/events/) for the lists of search parameters and event fields available.

## Running Tests

```Shell
pip install tox
tox
```

## Found a Bug?

Please [log an issue](https://github.com/predicthq/sdk-py/issues/new>).

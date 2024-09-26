# V3 breaking changes details

V3 introduces support for Python versions above 3.9 and drops support for Python 3.6.

In order to allow the following, we replaced the [Schematics](https://schematics.readthedocs.io/en/latest/) package (which is not maintained anymore and incompatible with python3.10+) by [Pydantic](https://docs.pydantic.dev/latest/).

We used to perform data validation on query params before sending the request to our API. This has been dropped in order to let our API validate query parameters as it's meant to.

The above induced a few breaking changes from prior versions. If you are migrating from version 2.4.0 or below to version 3.0.0 or above, please, take the time to read the following.

## No more support for Python3.6
As stated above, from version 3.0.0 onward, our SDK won't be available for python version below `3.7`.

## Fetched objects methods changed
The SDK endpoints used to return `Schematics` objects. They now return `Pydantic` objects.

Here follows a list of functions that won't be accessible on returned objects anymore and their pydantic equivalent:

| Schematics Method Name | Pydantic Equivalent |
|------------------------|---------------------|
| `obj.flatten()`          | ❌ |
| `obj.items()` | `list(obj.model_dump().items())`|
| `obj.iter()` | `obj.model_dump().items()` |
| `obj.keys()` | `obj.model_fields_set()` or `list(obj.model_fields_set())` if you need it to be a list of strings |
| `obj.serialize()` | `obj.model_dump()` or `json.loads(obj.model_dump_json())` if you wish to have dates as strings and not datetimes |
| `obj.to_dict()` | `obj.model_dump()` |
| `obj.to_native()` | ❌ |
| `obj.to_primitive()` | ❌ (behaves the same as `model_dump`) |
| `obj.values()` | `list(dict(obj).values())` |

For more `Pydantic` objects available methods, please check out [Pydantic Documentation](https://docs.pydantic.dev/latest/usage/models/#model-methods-and-properties).

*Note*: Pydantic will serialize all fields present on the models. If you wish to exclude `None` fields or fields that were missing from the API responses, use the `exclude_none=True` or `exclude_unset=True` function parameters when using the [model_dump](https://docs.pydantic.dev/latest/api/base_model/#pydantic.main.BaseModel.model_dump) and [model_json_dump](https://docs.pydantic.dev/latest/api/base_model/#pydantic.main.BaseModel.model_dump_json) functions.

Please do not hesitate to lodge an [issue](https://github.com/predicthq/sdk-py/issues) if any valuable behaviour that you were using through `schematics` objects are not achievable through `pydantic` objects.


## Event Search `within` parameter
When using the `within` query parameter for searching events, we used to allow multiple ways of providing the data for this filter:
```python
phq.events.search(within="10km@-36.844480,174.768368")
phq.events.search(within={"radius": "2km", "longitude": -71.0432, "latitude": 42.346})
phq.events.search(within__radius="2km", within__longitude=-71.0432, within__latitude=42.346)
```

Since we are not loading the query params data into objects and not validating it anymore, only the first example will be available from now on (which is the format described in [our documentation](https://docs.predicthq.com/api/events/search-events))

So if you were using the `within` filter sequentially, using `__` or with a dictionary, you will need to update it as follows
```python
phq.events.search(within="10km@-36.844480,174.768368")
```

## Exception update
Previously, if you would provide an incorect parameter to an endpoint, the method would raise a `predicthq.exceptions.ValidationError`.

This error would be formatted as follows
```
predicthq.exceptions.ValidationError: {'<field_name>': '<reason>'}
```

Since we are not performing validation within the SDK, the raised exception will instead contain the error message provided by our API.

The exception type has also been changed from `predicthq.exceptions.ValidationError` to `predicthq.exceptions.ClientError`.

Those errors will be formatted as follows
```
{'error': '<API Error description>', 'code': 400}
```

## Cannot use classes as query parameters anymore
Our endpoints used to allow users to use a `schematics` instance as a query parameter when querying our APIs.

e.g.
```python
from predicthq import Client
from predicthq.endpoints.v1.events.schemas import SearchParams

phq = Client(access_token="abc123")

query_params = SearchParams().import_data({
    "q": "Katy Perry",
    "state": ["active"],
    "rank_level": [4, 5],
    "category": "concerts"
})

for event in phq.events.search(query_params):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))
```

This feature was undocumented, so we are not expecting many or anyone to have used it ever.

In the unlikely event that you were using those, you will need to update it as one of the following as this is not supported anymore

```python
from predicthq import Client
from predicthq.endpoints.v1.events.schemas import SearchParams

phq = Client(access_token="abc123")

query_params = {
    "q": "Katy Perry",
    "state": ["active"],
    "rank_level": [4, 5],
    "category": "concerts"
}

# Either

for event in phq.events.search(**query_params):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))

# OR

for event in phq.events.search(q="Katy Perry", state=["active"], rank_level=[4, 5], category="concerts"):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))

```

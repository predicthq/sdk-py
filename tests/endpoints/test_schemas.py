import pytest
from typing import List

from pydantic import BaseModel, ValidationError

from predicthq.endpoints import decorators, schemas
from predicthq.endpoints.oauth2.schemas import AccessToken
from predicthq.endpoints.v1.events.schemas import PHQLabels
from predicthq.endpoints.v1.places.schemas import Place
from predicthq.endpoints.base import BaseEndpoint


def test_access_token_schema():
    with pytest.raises(ValidationError):
        AccessToken(access_token="some_access_token", token_type="some_token_type", scope=123)

    assert AccessToken(access_token="some_access_token", token_type="some_token_type", scope="some_scope").scope == ["some_scope"]

    assert AccessToken(access_token="some_access_token", token_type="some_token_type", scope="some scope").scope == ["some", "scope"]

    assert AccessToken(access_token="some_access_token", token_type="some_token_type", scope=["some" "scope"]).scope == ["some" "scope"]


def test_place_schema():
    with pytest.raises(ValidationError):
        Place(id="some_id", type="some_type", name="some_name", location=(1, 2, 3))

    with pytest.raises(ValidationError):
        Place(id="some_id", type="some_type", name="some_name", location=("a", "b"))

    assert Place(id="some_id", type="some_type", name="some_name", location=(32.123, -84.123)).location == (32.123, -84.123)

    assert Place(id="some_id", type="some_type", name="some_name", location=[32.123, -84.123]).location == (32.123, -84.123)


@pytest.mark.parametrize("phq_labels,raise_validation_error", [({"label": 34, "weight": "holiday"}, True),  # wrong type
                                                               ({"label": "holiday", "weight": "holiday"}, True),  # wrong type
                                                               ({"label": 34, "weight": 6}, True),  # wrong type
                                                               ({"weight": 2.0}, True),  # missing label
                                                               ({"label": "holiday"}, True),  # missing weight
                                                               ({"label": "some_string", "weight": 2.0}, False),  # correct
                                                               ({"label": "another_string", "weight": 7}, False)])  # correct
def test_phq_label_schema(phq_labels, raise_validation_error):
    if raise_validation_error:
        with pytest.raises(ValidationError) as e:
            label = PHQLabels.parse_obj(phq_labels)
    else:
        label = PHQLabels.parse_obj(phq_labels)
        assert label.label == phq_labels["label"]
        assert label.weight == phq_labels["weight"]


def test_resultset():
    class ResultExample(BaseModel):
        value: int

    class ResultSetExample(schemas.ResultSet):
        results: List[ResultExample]

    class EndpointExample(BaseEndpoint):
        @decorators.returns(ResultSetExample)
        def load_page(self, page):
            page = int(page)
            return {
                "count": 9,
                "next": f"http://example.org/?page={page + 1}" if page < 3 else None,
                "previous": f"http://example.org/?page={page - 1}" if page > 1 else None,
                "results": [
                    {"value": 1 + (3 * (page - 1))},
                    {"value": 2 + (3 * (page - 1))},
                    {"value": 3 + (3 * (page - 1))},
                ],
            }

    endpoint = EndpointExample(None)

    p1 = endpoint.load_page(page=1)
    assert p1.count == 9
    assert list(p1) == [ResultExample(**{"value": 1}), ResultExample(**{"value": 2}), ResultExample(**{"value": 3})]
    assert p1.has_previous() is False
    assert p1.has_next() is True
    assert p1.get_previous() is None

    p2 = p1.get_next()

    assert list(p2) == [ResultExample(**{"value": 4}), ResultExample(**{"value": 5}), ResultExample(**{"value": 6})]
    assert p2.has_previous() is True
    assert p2.has_next() is True

    p3 = p2.get_next()
    assert list(p3) == [ResultExample(**{"value": 7}), ResultExample(**{"value": 8}), ResultExample(**{"value": 9})]
    assert p3.has_previous() is True
    assert p3.has_next() is False

    assert p3.get_next() is None
    assert list(p3.get_previous()) == list(p2)

    assert [x.model_dump() for x in p1.iter_pages()] == [endpoint.load_page(page=2).model_dump(), endpoint.load_page(page=3).model_dump()]
    assert list(p1.iter_all()) == list(p1) + list(p2) + list(p3)

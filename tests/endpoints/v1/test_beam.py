import unittest

from tests import load_fixture, with_mock_client
from predicthq.endpoints.v1.beam.schemas import (
    FeatureImportance,
    CorrelationResultSet,
    Analysis,
    CreateAnalysisResponse,
    CreateAnalysisGroupResponse,
    AnalysisResultSet,
    AnalysisGroupResultSet,
    AnalysisGroup,
)


class BeamTest(unittest.TestCase):
    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_search"))
    def test_search(self, client):
        result = client.beam.analysis.search()

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/",
            params={},
            verify=True,
        )

        assert isinstance(result, AnalysisResultSet)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_search"))
    def test_search_params_underscores(self, client):
        client.beam.analysis.search(
            updated__gt="2016-03-01",
            updated__gte="2016-03-01",
            updated__lt="2016-04-01",
            updated__lte="2016-04-01",
            q="query",
            status="active",
            group_id="group_id",
            demand_type__interval="week",
            demand_type__industry="retail",
            readiness_status=["ready", "not_ready"],
            include_deleted=True,
            sort=["rank", "-start"],
            offset=10,
            limit=10,
            external_id="external_id",
            label=["label1", "label2"],
            location__saved_location_id="saved_location_id",
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/",
            params={
                "updated.gt": "2016-03-01",
                "updated.gte": "2016-03-01",
                "updated.lt": "2016-04-01",
                "updated.lte": "2016-04-01",
                "q": "query",
                "status": "active",
                "group_id": "group_id",
                "demand_type.interval": "week",
                "demand_type.industry": "retail",
                "readiness_status": "ready,not_ready",
                "include_deleted": 1,
                "sort": "rank,-start",
                "offset": 10,
                "limit": 10,
                "external_id": "external_id",
                "label": "label1,label2",
                "location.saved_location_id": "saved_location_id",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_search"))
    def test_search_params_dicts(self, client):
        client.beam.analysis.search(
            updated={
                "gt": "2016-03-01",
                "gte": "2016-03-01",
                "lt": "2016-04-01",
                "lte": "2016-04-01",
            },
            q="query",
            status="active",
            group_id="group_id",
            demand_type={"interval": "week", "industry": "retail"},
            readiness_status=["ready", "not_ready"],
            include_deleted=True,
            sort=["rank", "-start"],
            offset=10,
            limit=10,
            external_id="external_id",
            label=["label1", "label2"],
            location__saved_location_id="saved_location_id",
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/",
            params={
                "updated.gt": "2016-03-01",
                "updated.gte": "2016-03-01",
                "updated.lt": "2016-04-01",
                "updated.lte": "2016-04-01",
                "q": "query",
                "status": "active",
                "group_id": "group_id",
                "demand_type.interval": "week",
                "demand_type.industry": "retail",
                "readiness_status": "ready,not_ready",
                "include_deleted": 1,
                "sort": "rank,-start",
                "offset": 10,
                "limit": 10,
                "external_id": "external_id",
                "label": "label1,label2",
                "location.saved_location_id": "saved_location_id",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_create"))
    def test_create_params_underscores(self, client):
        result = client.beam.analysis.create(
            name="name",
            location__geopoint={"lat": 1.1, "lon": 1.2},
            location__radius=1.0,
            location__unit="km",
            location__google_place_id="google_place_id",
            location__geoscope_paths=["geoscope_path1", "geoscope_path2"],
            location__saved_location_id="saved_location_id",
            rank__type="type",
            rank__levels__phq={"min": 1.0, "max": 2.0},
            rank__levels__local={"min": 3.0, "max": 4.0},
            demand_type__industry="industry",
            demand_type__unit_descriptor="unit_descriptor",
            demand_type__unit_currency_multiplier=1.4,
            demand_type__currency_code="currency_code",
            tz="tz",
            external_id="external_id",
            label=["label1", "label2"],
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/beam/analyses/",
            json={
                "name": "name",
                "location": {
                    "geopoint": {"lat": 1.1, "lon": 1.2},
                    "radius": 1.0,
                    "unit": "km",
                    "google_place_id": "google_place_id",
                    "geoscope_paths": ["geoscope_path1", "geoscope_path2"],
                    "saved_location_id": "saved_location_id",
                },
                "rank": {
                    "type": "type",
                    "levels": {
                        "phq": {"min": 1.0, "max": 2.0},
                        "local": {"min": 3.0, "max": 4.0},
                    },
                },
                "demand_type": {
                    "industry": "industry",
                    "unit_descriptor": "unit_descriptor",
                    "unit_currency_multiplier": 1.4,
                    "currency_code": "currency_code",
                },
                "tz": "tz",
                "external_id": "external_id",
                "label": ["label1", "label2"],
            },
            verify=True,
        )
        assert isinstance(result, CreateAnalysisResponse)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_create"))
    def test_create_params_dicts(self, client):
        result = client.beam.analysis.create(
            name="name",
            location={
                "geopoint": {"lat": 1.1, "lon": 1.2},
                "radius": 1.0,
                "unit": "km",
                "google_place_id": "google_place_id",
                "geoscope_paths": ["geoscope_path1", "geoscope_path2"],
                "saved_location_id": "saved_location_id",
            },
            rank={
                "type": "type",
                "levels": {
                    "phq": {"min": 1.0, "max": 2.0},
                    "local": {"min": 3.0, "max": 4.0},
                },
            },
            demand_type={
                "industry": "industry",
                "unit_descriptor": "unit_descriptor",
                "unit_currency_multiplier": 1.4,
                "currency_code": "currency_code",
            },
            tz="tz",
            external_id="external_id",
            label=["label1", "label2"],
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/beam/analyses/",
            json={
                "name": "name",
                "location": {
                    "geopoint": {"lat": 1.1, "lon": 1.2},
                    "radius": 1.0,
                    "unit": "km",
                    "google_place_id": "google_place_id",
                    "geoscope_paths": ["geoscope_path1", "geoscope_path2"],
                    "saved_location_id": "saved_location_id",
                },
                "rank": {
                    "type": "type",
                    "levels": {
                        "phq": {"min": 1.0, "max": 2.0},
                        "local": {"min": 3.0, "max": 4.0},
                    },
                },
                "demand_type": {
                    "industry": "industry",
                    "unit_descriptor": "unit_descriptor",
                    "unit_currency_multiplier": 1.4,
                    "currency_code": "currency_code",
                },
                "tz": "tz",
                "external_id": "external_id",
                "label": ["label1", "label2"],
            },
            verify=True,
        )

        assert isinstance(result, CreateAnalysisResponse)

    @with_mock_client()
    def test_update_params_underscores(self, client):
        client.beam.analysis.update(
            analysis_id="abc123",
            name="name",
            location__geopoint={"lat": 1.1, "lon": 1.2},
            location__radius=1.0,
            location__unit="km",
            location__google_place_id="google_place_id",
            location__geoscope_paths=["geoscope_path1", "geoscope_path2"],
            location__saved_location_id="saved_location_id",
            rank__type="type",
            rank__levels__phq={"min": 1.0, "max": 2.0},
            rank__levels__local={"min": 3.0, "max": 4.0},
            demand_type__industry="industry",
            demand_type__unit_descriptor="unit_descriptor",
            demand_type__unit_currency_multiplier=1.4,
            demand_type__currency_code="currency_code",
            tz="tz",
            external_id="external_id",
            label=["label1", "label2"],
        )

        client.request.assert_called_once_with(
            "patch",
            "/v1/beam/analyses/abc123/",
            json={
                "name": "name",
                "location": {
                    "geopoint": {"lat": 1.1, "lon": 1.2},
                    "radius": 1.0,
                    "unit": "km",
                    "google_place_id": "google_place_id",
                    "geoscope_paths": ["geoscope_path1", "geoscope_path2"],
                    "saved_location_id": "saved_location_id",
                },
                "rank": {
                    "type": "type",
                    "levels": {
                        "phq": {"min": 1.0, "max": 2.0},
                        "local": {"min": 3.0, "max": 4.0},
                    },
                },
                "demand_type": {
                    "industry": "industry",
                    "unit_descriptor": "unit_descriptor",
                    "unit_currency_multiplier": 1.4,
                    "currency_code": "currency_code",
                },
                "tz": "tz",
                "external_id": "external_id",
                "label": ["label1", "label2"],
            },
            verify=True,
        )

    @with_mock_client()
    def test_update_params_dicts(self, client):
        client.beam.analysis.update(
            analysis_id="abc123",
            name="name",
            location={
                "geopoint": {"lat": 1.1, "lon": 1.2},
                "radius": 1.0,
                "unit": "km",
                "google_place_id": "google_place_id",
                "geoscope_paths": ["geoscope_path1", "geoscope_path2"],
                "saved_location_id": "saved_location_id",
            },
            rank={
                "type": "type",
                "levels": {
                    "phq": {"min": 1.0, "max": 2.0},
                    "local": {"min": 3.0, "max": 4.0},
                },
            },
            demand_type={
                "industry": "industry",
                "unit_descriptor": "unit_descriptor",
                "unit_currency_multiplier": 1.4,
                "currency_code": "currency_code",
            },
            tz="tz",
            external_id="external_id",
            label=["label1", "label2"],
        )

        client.request.assert_called_once_with(
            "patch",
            "/v1/beam/analyses/abc123/",
            json={
                "name": "name",
                "location": {
                    "geopoint": {"lat": 1.1, "lon": 1.2},
                    "radius": 1.0,
                    "unit": "km",
                    "google_place_id": "google_place_id",
                    "geoscope_paths": ["geoscope_path1", "geoscope_path2"],
                    "saved_location_id": "saved_location_id",
                },
                "rank": {
                    "type": "type",
                    "levels": {
                        "phq": {"min": 1.0, "max": 2.0},
                        "local": {"min": 3.0, "max": 4.0},
                    },
                },
                "demand_type": {
                    "industry": "industry",
                    "unit_descriptor": "unit_descriptor",
                    "unit_currency_multiplier": 1.4,
                    "currency_code": "currency_code",
                },
                "tz": "tz",
                "external_id": "external_id",
                "label": ["label1", "label2"],
            },
            verify=True,
        )

    @with_mock_client()
    def test_delete(self, client):
        client.beam.analysis.delete(analysis_id="abc123")

        client.request.assert_called_once_with(
            "delete",
            "/v1/beam/analyses/abc123/",
            params={},
            verify=True,
        )

    @with_mock_client()
    def test_refresh(self, client):
        client.beam.analysis.refresh(analysis_id="abc123")

        client.request.assert_called_once_with(
            "post",
            "/v1/beam/analyses/abc123/refresh/",
            params={},
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_correlation"))
    def test_get_correlation_results_params_underscores(self, client):
        client.beam.analysis.get_correlation_results(
            analysis_id="abc123",
            date__gt="2024-01-01",
            date__gte="2024-01-01",
            date__lt="2024-01-31",
            date__lte="2024-01-31",
            offset=10,
            limit=10,
            include_features=["feature1", "feature2"],
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/abc123/correlate/",
            params={
                "date.gt": "2024-01-01",
                "date.gte": "2024-01-01",
                "date.lt": "2024-01-31",
                "date.lte": "2024-01-31",
                "offset": 10,
                "limit": 10,
                "include_features": "feature1,feature2",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_correlation"))
    def test_get_correlation_results_empty_params_dicts(self, client):
        client.beam.analysis.get_correlation_results(
            analysis_id="abc123",
            date={
                "gt": "2024-01-01",
                "gte": "2024-01-01",
                "lt": "2024-01-31",
                "lte": "2024-01-31",
            },
            offset=10,
            limit=10,
            include_features=["feature1", "feature2"],
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/abc123/correlate/",
            params={
                "date.gt": "2024-01-01",
                "date.gte": "2024-01-01",
                "date.lt": "2024-01-31",
                "date.lte": "2024-01-31",
                "offset": 10,
                "limit": 10,
                "include_features": "feature1,feature2",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_correlation"))
    def test_get_correlation_results_params_dicts(self, client):
        result = client.beam.analysis.get_correlation_results(
            analysis_id="abc123",
            date={
                "gt": "2024-01-01",
                "gte": "2024-01-01",
                "lt": "2024-01-31",
                "lte": "2024-01-31",
            },
            offset=10,
            limit=10,
            include_features=["feature1", "feature2"],
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/abc123/correlate/",
            params={
                "date.gt": "2024-01-01",
                "date.gte": "2024-01-01",
                "date.lt": "2024-01-31",
                "date.lte": "2024-01-31",
                "offset": 10,
                "limit": 10,
                "include_features": "feature1,feature2",
            },
            verify=True,
        )

        assert isinstance(result, CorrelationResultSet)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_feature_importance"))
    def test_feature_empty_importance(self, client):
        client.beam.analysis.get_feature_importance(analysis_id="abc123")

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/abc123/feature-importance/",
            params={},
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_feature_importance"))
    def test_feature_importance(self, client):
        result = client.beam.analysis.get_feature_importance(analysis_id="abc123")

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/abc123/feature-importance/",
            params={},
            verify=True,
        )
        assert isinstance(result, FeatureImportance)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_analysis"))
    def test_get_analysis(self, client):
        result = client.beam.analysis.get(analysis_id="abc123")

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analyses/abc123/",
            params={},
            verify=True,
        )
        assert isinstance(result, Analysis)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_create_group"))
    def test_create_group_params_underscores(self, client):
        result = client.beam.analysis_group.create(
            name="name",
            analysis_ids=["analysis_id1", "analysis_id2"],
            demand_type__unit_descriptor="unit_descriptor",
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/beam/analysis-groups/",
            json={
                "name": "name",
                "analysis_ids": ["analysis_id1", "analysis_id2"],
                "demand_type": {"unit_descriptor": "unit_descriptor"},
            },
            verify=True,
        )

        assert isinstance(result, CreateAnalysisGroupResponse)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_create_group"))
    def test_create_group_params_dicts(self, client):
        result = client.beam.analysis_group.create(
            name="name",
            analysis_ids=["analysis_id1", "analysis_id2"],
            demand_type={"unit_descriptor": "unit_descriptor"},
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/beam/analysis-groups/",
            json={
                "name": "name",
                "analysis_ids": ["analysis_id1", "analysis_id2"],
                "demand_type": {"unit_descriptor": "unit_descriptor"},
            },
            verify=True,
        )

        assert isinstance(result, CreateAnalysisGroupResponse)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_group_search"))
    def test_search_group(self, client):
        result = client.beam.analysis_group.search()

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analysis-groups/",
            params={},
            verify=True,
        )

        assert isinstance(result, AnalysisGroupResultSet)

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_group_search"))
    def test_search_group_params_underscores(self, client):
        client.beam.analysis_group.search(
            updated__gt="2016-03-01",
            updated__gte="2016-03-01",
            updated__lt="2016-04-01",
            updated__lte="2016-04-01",
            q="query",
            status=["active", "inactive"],
            demand_type__interval=["week", "month"],
            demand_type__industry=["retail", "hospitality"],
            readiness_status=["ready", "not_ready"],
            include_deleted=True,
            sort=["rank", "-start"],
            offset=10,
            limit=10,
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analysis-groups/",
            params={
                "updated.gt": "2016-03-01",
                "updated.gte": "2016-03-01",
                "updated.lt": "2016-04-01",
                "updated.lte": "2016-04-01",
                "q": "query",
                "status": "active,inactive",
                "demand_type.interval": "week,month",
                "demand_type.industry": "retail,hospitality",
                "readiness_status": "ready,not_ready",
                "include_deleted": 1,
                "sort": "rank,-start",
                "offset": 10,
                "limit": 10,
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_group_search"))
    def test_search_group_params_dicts(self, client):
        client.beam.analysis_group.search(
            updated={
                "gt": "2016-03-01",
                "gte": "2016-03-01",
                "lt": "2016-04-01",
                "lte": "2016-04-01",
            },
            q="query",
            status="active,inactive",
            demand_type={
                "interval": "week,month",
                "industry": "retail,hospitality",
            },
            readiness_status="ready,not_ready",
            include_deleted=1,
            sort="rank,-start",
            offset=10,
            limit=10,
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analysis-groups/",
            params={
                "updated.gt": "2016-03-01",
                "updated.gte": "2016-03-01",
                "updated.lt": "2016-04-01",
                "updated.lte": "2016-04-01",
                "q": "query",
                "status": "active,inactive",
                "demand_type.interval": "week,month",
                "demand_type.industry": "retail,hospitality",
                "readiness_status": "ready,not_ready",
                "include_deleted": 1,
                "sort": "rank,-start",
                "offset": 10,
                "limit": 10,
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_analysis_group"))
    def test_get_analysis_group(self, client):
        result = client.beam.analysis_group.get(group_id="abc123")

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analysis-groups/abc123/",
            params={},
            verify=True,
        )
        assert isinstance(result, AnalysisGroup)

    @with_mock_client()
    def test_update_group_params_underscores(self, client):
        client.beam.analysis_group.update(
            group_id="abc123",
            name="name",
            analysis_ids=["analysis_id1", "analysis_id2"],
            demand_type__unit_descriptor="unit_descriptor",
        )

        client.request.assert_called_once_with(
            "patch",
            "/v1/beam/analysis-groups/abc123/",
            json={
                "name": "name",
                "analysis_ids": ["analysis_id1", "analysis_id2"],
                "demand_type": {"unit_descriptor": "unit_descriptor"},
            },
            verify=True,
        )

    @with_mock_client()
    def test_update_group_params_dicts(self, client):
        client.beam.analysis_group.update(
            group_id="abc123",
            name="name",
            analysis_ids=["analysis_id1", "analysis_id2"],
            demand_type={"unit_descriptor": "unit_descriptor"},
        )

        client.request.assert_called_once_with(
            "patch",
            "/v1/beam/analysis-groups/abc123/",
            json={
                "name": "name",
                "analysis_ids": ["analysis_id1", "analysis_id2"],
                "demand_type": {"unit_descriptor": "unit_descriptor"},
            },
            verify=True,
        )

    @with_mock_client()
    def test_delete_group(self, client):
        client.beam.analysis_group.delete(group_id="abc123")

        client.request.assert_called_once_with(
            "delete",
            "/v1/beam/analysis-groups/abc123/",
            params={},
            verify=True,
        )

    @with_mock_client()
    def test_refresh_group(self, client):
        client.beam.analysis_group.refresh(group_id="abc123")

        client.request.assert_called_once_with(
            "post",
            "/v1/beam/analysis-groups/abc123/refresh/",
            params={},
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_empty_feature_importance"))
    def test_group_feature_empty_importance(self, client):
        client.beam.analysis_group.get_feature_importance(group_id="abc123")

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analysis-groups/abc123/feature-importance/",
            params={},
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/beam_test/test_feature_importance"))
    def test_group_feature_importance(self, client):
        result = client.beam.analysis_group.get_feature_importance(group_id="abc123")

        client.request.assert_called_once_with(
            "get",
            "/v1/beam/analysis-groups/abc123/feature-importance/",
            params={},
            verify=True,
        )
        assert isinstance(result, FeatureImportance)

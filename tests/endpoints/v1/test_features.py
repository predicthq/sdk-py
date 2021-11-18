import unittest

from predicthq.endpoints.v1.features.schemas import FeatureResultSet
from tests import with_mock_client, with_mock_responses, with_client


class FeaturesTest(unittest.TestCase):
    @with_mock_client()
    def test_mutate_default_criteria(self, client):
        client.features.obtain_features(
            active__gte="2021-01-01",
            active__lte="2021-01-30",
            location={"geo": {"lon": -93.151959, "lat": 44.835976, "radius": "2km"}},
            phq_attendance_conferences=True,
            phq_attendance_performing_arts=True,
            phq_viewership_sports=True,
            phq_viewership_sports_american_football=True,
            phq_viewership_sports_boxing=True,
            phq_viewership_sports_basketball_nba=True,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2021-01-01", "lte": "2021-01-30"},
                "location": {"geo": {"lat": 44.835976, "lon": -93.151959, "radius": "2km"}},
                "phq_attendance_conferences": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_attendance_performing_arts": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports_american_football": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports_boxing": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports_basketball_nba": {"stats": ["sum", "count"], "phq_rank": None},
            },
        )

    @with_mock_client()
    def test_attendance_request_params_underscores(self, client):
        feature_stats = ["avg", "count", "max", "median", "min", "sum", "std_dev"]
        client.features.obtain_features(
            active__gte="2017-12-31",
            active__lte="2018-01-02",
            location__place_id=[4671654],
            phq_attendance_academic_graduation__stats=feature_stats,
            phq_attendance_academic_graduation__phq_rank={"gt": 50},
            phq_attendance_academic_social__stats=feature_stats,
            phq_attendance_community__stats=feature_stats,
            phq_attendance_concerts__stats=feature_stats,
            phq_attendance_conferences__stats=feature_stats,
            phq_attendance_expos__stats=feature_stats,
            phq_attendance_festivals__stats=feature_stats,
            phq_attendance_performing_arts__stats=feature_stats,
            phq_attendance_sports__stats=feature_stats,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "location": {"place_id": ["4671654"]},
                "phq_attendance_academic_graduation": {"stats": feature_stats, "phq_rank": {"gt": 50}},
                "phq_attendance_academic_social": {"stats": feature_stats},
                "phq_attendance_community": {"stats": feature_stats},
                "phq_attendance_concerts": {"stats": feature_stats},
                "phq_attendance_conferences": {"stats": feature_stats},
                "phq_attendance_expos": {"stats": feature_stats},
                "phq_attendance_festivals": {"stats": feature_stats},
                "phq_attendance_performing_arts": {"stats": feature_stats},
                "phq_attendance_sports": {"stats": feature_stats},
            },
        )

    @with_mock_client()
    def test_attendance_request_params_dicts(self, client):
        feature_criteria = {"stats": ["avg", "count", "max", "median", "min", "sum", "std_dev"], "phq_rank": {"gt": 50}}
        client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            location={"geo": {"lon": -71.49978, "lat": 41.75038, "radius": "30km"}},
            phq_attendance_academic_graduation=feature_criteria,
            phq_attendance_academic_social=feature_criteria,
            phq_attendance_community=feature_criteria,
            phq_attendance_concerts=feature_criteria,
            phq_attendance_conferences=feature_criteria,
            phq_attendance_expos=feature_criteria,
            phq_attendance_festivals=feature_criteria,
            phq_attendance_performing_arts=feature_criteria,
            phq_attendance_sports=feature_criteria,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
                "phq_attendance_academic_graduation": feature_criteria,
                "phq_attendance_academic_social": feature_criteria,
                "phq_attendance_community": feature_criteria,
                "phq_attendance_concerts": feature_criteria,
                "phq_attendance_conferences": feature_criteria,
                "phq_attendance_expos": feature_criteria,
                "phq_attendance_festivals": feature_criteria,
                "phq_attendance_performing_arts": feature_criteria,
                "phq_attendance_sports": feature_criteria,
            },
        )

    @with_mock_client()
    def test_rank_request_params_underscores(self, client):
        client.features.obtain_features(
            active__gte="2017-12-31",
            active__lte="2018-01-02",
            location__geo={"lon": -71.49978, "lat": 41.75038, "radius": "30km"},
            phq_rank_daylight_savings=True,
            phq_rank_health_warnings=True,
            phq_rank_observances=True,
            phq_rank_public_holidays=True,
            phq_rank_school_holidays=True,
            phq_rank_politics=True,
            phq_rank_academic_session=True,
            phq_rank_academic_exam=True,
            phq_rank_academic_holiday=True,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
                "phq_rank_daylight_savings": True,
                "phq_rank_health_warnings": True,
                "phq_rank_observances": True,
                "phq_rank_public_holidays": True,
                "phq_rank_school_holidays": True,
                "phq_rank_politics": True,
                "phq_rank_academic_session": True,
                "phq_rank_academic_exam": True,
                "phq_rank_academic_holiday": True,
            },
        )

    @with_mock_client()
    def test_rank_request_params_dicts(self, client):
        client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            location={"place_id": [4671654]},
            phq_rank_daylight_savings=True,
            phq_rank_health_warnings=True,
            phq_rank_observances=True,
            phq_rank_public_holidays=True,
            phq_rank_school_holidays=True,
            phq_rank_politics=True,
            phq_rank_academic_session=True,
            phq_rank_academic_exam=True,
            phq_rank_academic_holiday=True,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "location": {"place_id": ["4671654"]},
                "phq_rank_daylight_savings": True,
                "phq_rank_health_warnings": True,
                "phq_rank_observances": True,
                "phq_rank_public_holidays": True,
                "phq_rank_school_holidays": True,
                "phq_rank_politics": True,
                "phq_rank_academic_session": True,
                "phq_rank_academic_exam": True,
                "phq_rank_academic_holiday": True,
            },
        )

    @with_client()
    @with_mock_responses()
    def test_obtain_features(self, client, responses):
        result = client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            location={"place_id": [4671654]},
            phq_rank_public_holidays=True,
        )
        assert isinstance(result, FeatureResultSet)

    @with_mock_client()
    def test_viewership_request_params_underscores(self, client):
        feature_stats = ["avg", "count", "max", "median", "min", "sum", "std_dev"]
        client.features.obtain_features(
            active__gte="2017-12-31",
            active__lte="2018-01-02",
            hour_of_day_active__gt=10,
            hour_of_day_active__lte=19,
            location__place_id=[4671654],
            phq_viewership_sports__stats=feature_stats,
            phq_viewership_sports__phq_rank={"gt": 50},
            phq_viewership_sports_american_football__stats=feature_stats,
            phq_viewership_sports_american_football__phq_rank={"gt": 50},
            phq_viewership_sports_baseball_mlb__stats=feature_stats,
            phq_viewership_sports_basketball__stats=feature_stats,
            phq_viewership_sports_ice_hockey_nhl__stats=feature_stats,
            phq_viewership_sports_soccer__stats=feature_stats,
            phq_viewership_sports_golf_pga_championship__stats=feature_stats,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "hour_of_day_active": {"gt": 10, "lte": 19},
                "location": {"place_id": ["4671654"]},
                "phq_viewership_sports": {"stats": feature_stats, "phq_rank": {"gt": 50}},
                "phq_viewership_sports_american_football": {"stats": feature_stats, "phq_rank": {"gt": 50}},
                "phq_viewership_sports_baseball_mlb": {"stats": feature_stats},
                "phq_viewership_sports_basketball": {"stats": feature_stats},
                "phq_viewership_sports_ice_hockey_nhl": {"stats": feature_stats},
                "phq_viewership_sports_soccer": {"stats": feature_stats},
                "phq_viewership_sports_golf_pga_championship": {"stats": feature_stats},
            },
        )

    @with_mock_client()
    def test_viewership_request_params_dicts(self, client):
        feature_criteria = {"stats": ["avg", "count", "max", "median", "min", "sum", "std_dev"], "phq_rank": {"gt": 50}}
        client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            hour_of_day_start={"gte": 10, "lt": 11},
            location={"geo": {"lon": -71.49978, "lat": 41.75038, "radius": "30km"}},
            phq_viewership_sports_american_football_ncaa_men=feature_criteria,
            phq_viewership_sports_baseball=feature_criteria,
            phq_viewership_sports_basketball_ncaa_men=feature_criteria,
            phq_viewership_sports_basketball_nba=feature_criteria,
            phq_viewership_sports_ice_hockey_nhl=feature_criteria,
            phq_viewership_sports_soccer_mls=feature_criteria,
            phq_viewership_sports_auto_racing=feature_criteria,
            phq_viewership_sports_horse_racing=feature_criteria,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "hour_of_day_start": {"gte": 10, "lt": 11},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
                "phq_viewership_sports_american_football_ncaa_men": feature_criteria,
                "phq_viewership_sports_baseball": feature_criteria,
                "phq_viewership_sports_basketball_ncaa_men": feature_criteria,
                "phq_viewership_sports_basketball_nba": feature_criteria,
                "phq_viewership_sports_ice_hockey_nhl": feature_criteria,
                "phq_viewership_sports_soccer_mls": feature_criteria,
                "phq_viewership_sports_auto_racing": feature_criteria,
                "phq_viewership_sports_horse_racing": feature_criteria,
            },
        )

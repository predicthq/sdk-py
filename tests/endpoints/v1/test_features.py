import unittest

from predicthq.endpoints.v1.features.schemas import FeatureResultSet
from tests import load_fixture, with_client, with_mock_client, with_mock_responses


class FeaturesTest(unittest.TestCase):
    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_mutate_default_criteria(self, client):
        client.features.obtain_features(
            active__gte="2021-01-01",
            active__lte="2021-01-30",
            location={"geo": {"lon": -93.151959, "lat": 44.835976, "radius": "2km"}},
            phq_attendance_conferences=True,
            phq_attendance_performing_arts=True,
            phq_attendance_performing_arts_accommodation=True,
            phq_attendance_performing_arts_hospitality=True,
            phq_impact_severe_weather_air_quality_retail=True,
            phq_viewership_sports=True,
            phq_viewership_sports_american_football=True,
            phq_viewership_sports_boxing=True,
            phq_viewership_sports_basketball_nba=True,
            phq_spend_expos=True,
            phq_spend_community_accommodation=True,
            phq_spend_festivals_hospitality=True,
            phq_spend_performing_arts_transportation=True,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2021-01-01", "lte": "2021-01-30"},
                "location": {"geo": {"lat": 44.835976, "lon": -93.151959, "radius": "2km"}},
                "phq_attendance_conferences": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_attendance_performing_arts": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_attendance_performing_arts_accommodation": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_attendance_performing_arts_hospitality": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_impact_severe_weather_air_quality_retail": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports_american_football": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports_boxing": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_viewership_sports_basketball_nba": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_spend_expos": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_spend_community_accommodation": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_spend_festivals_hospitality": {"stats": ["sum", "count"], "phq_rank": None},
                "phq_spend_performing_arts_transportation": {"stats": ["sum", "count"], "phq_rank": None},
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_attendance_request_params_underscores(self, client):
        feature_stats = ["avg", "count", "max", "median", "min", "sum", "std_dev"]
        client.features.obtain_features(
            active__gte="2017-12-31",
            active__lte="2018-01-02",
            location__place_id=["4671654"],
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
            phq_attendance_community_accommodation__stats=feature_stats,
            phq_attendance_concerts_accommodation__stats=feature_stats,
            phq_attendance_conferences_accommodation__stats=feature_stats,
            phq_attendance_expos_accommodation__stats=feature_stats,
            phq_attendance_festivals_accommodation__stats=feature_stats,
            phq_attendance_performing_arts_accommodation__stats=feature_stats,
            phq_attendance_sports_accommodation__stats=feature_stats,
            phq_attendance_community_hospitality__stats=feature_stats,
            phq_attendance_concerts_hospitality__stats=feature_stats,
            phq_attendance_conferences_hospitality__stats=feature_stats,
            phq_attendance_expos_hospitality__stats=feature_stats,
            phq_attendance_festivals_hospitality__stats=feature_stats,
            phq_attendance_performing_arts_hospitality__stats=feature_stats,
            phq_attendance_sports_hospitality__stats=feature_stats,

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
                "phq_attendance_community_accommodation": {"stats": feature_stats},
                "phq_attendance_concerts_accommodation": {"stats": feature_stats},
                "phq_attendance_conferences_accommodation": {"stats": feature_stats},
                "phq_attendance_expos_accommodation": {"stats": feature_stats},
                "phq_attendance_festivals_accommodation": {"stats": feature_stats},
                "phq_attendance_performing_arts_accommodation": {"stats": feature_stats},
                "phq_attendance_sports_accommodation": {"stats": feature_stats},
                "phq_attendance_community_hospitality": {"stats": feature_stats},
                "phq_attendance_concerts_hospitality": {"stats": feature_stats},
                "phq_attendance_conferences_hospitality": {"stats": feature_stats},
                "phq_attendance_expos_hospitality": {"stats": feature_stats},
                "phq_attendance_festivals_hospitality": {"stats": feature_stats},
                "phq_attendance_performing_arts_hospitality": {"stats": feature_stats},
                "phq_attendance_sports_hospitality": {"stats": feature_stats},
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_attendance_request_params_underscores_without_ssl_verification(self, client):
        client.features.obtain_features(
            active__gte="2017-12-31", location__place_id=["4671654"], config__verify_ssl=False
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31"},
                "location": {"place_id": ["4671654"]},
            },
            verify=False,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
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
            phq_attendance_school_holidays=feature_criteria,
            phq_attendance_sports=feature_criteria,
            phq_attendance_community_accommodation=feature_criteria,
            phq_attendance_concerts_accommodation=feature_criteria,
            phq_attendance_conferences_accommodation=feature_criteria,
            phq_attendance_expos_accommodation=feature_criteria,
            phq_attendance_festivals_accommodation=feature_criteria,
            phq_attendance_performing_arts_accommodation=feature_criteria,
            phq_attendance_sports_accommodation=feature_criteria,
            phq_attendance_community_hospitality=feature_criteria,
            phq_attendance_concerts_hospitality=feature_criteria,
            phq_attendance_conferences_hospitality=feature_criteria,
            phq_attendance_expos_hospitality=feature_criteria,
            phq_attendance_festivals_hospitality=feature_criteria,
            phq_attendance_performing_arts_hospitality=feature_criteria,
            phq_attendance_sports_hospitality=feature_criteria,
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
                "phq_attendance_school_holidays": feature_criteria,
                "phq_attendance_sports": feature_criteria,
                "phq_attendance_community_accommodation": feature_criteria,
                "phq_attendance_concerts_accommodation": feature_criteria,
                "phq_attendance_conferences_accommodation": feature_criteria,
                "phq_attendance_expos_accommodation": feature_criteria,
                "phq_attendance_festivals_accommodation": feature_criteria,
                "phq_attendance_performing_arts_accommodation": feature_criteria,
                "phq_attendance_sports_accommodation": feature_criteria,
                "phq_attendance_community_hospitality": feature_criteria,
                "phq_attendance_concerts_hospitality": feature_criteria,
                "phq_attendance_conferences_hospitality": feature_criteria,
                "phq_attendance_expos_hospitality": feature_criteria,
                "phq_attendance_festivals_hospitality": feature_criteria,
                "phq_attendance_performing_arts_hospitality": feature_criteria,
                "phq_attendance_sports_hospitality": feature_criteria,
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_attendance_request_params_dicts_without_ssl_verification(self, client):
        client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            location={"geo": {"lon": -71.49978, "lat": 41.75038, "radius": "30km"}},
            config={"verify_ssl": False},
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
            },
            verify=False,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
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
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_rank_request_params_underscores_without_ssl_verification(self, client):
        client.features.obtain_features(
            active__gte="2017-12-31",
            location__geo={"lon": -71.49978, "lat": 41.75038, "radius": "30km"},
            config__verify_ssl=False,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31"},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
            },
            verify=False,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_rank_request_params_dicts(self, client):
        client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            location={"place_id": ["4671654"]},
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
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_rank_request_params_dicts_without_ssl_verification(self, client):
        client.features.obtain_features(
            active={"gte": "2017-12-31"}, location={"place_id": ["4671654"]}, config={"verify_ssl": False}
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31"},
                "location": {"place_id": ["4671654"]},
            },
            verify=False,
        )

    @with_client()
    @with_mock_responses()
    def test_obtain_features(self, client, responses):
        result = client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            location={"place_id": ["4671654"]},
            phq_rank_public_holidays=True,
        )
        assert isinstance(result, FeatureResultSet)

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_impact_severe_weather_request_params_underscores(self, client):
        feature_stats = ["avg", "count", "max", "median", "min", "sum", "std_dev"]
        client.features.obtain_features(
            active__gte="2017-12-31",
            active__lte="2018-01-02",
            hour_of_day_active__gt=10,
            hour_of_day_active__lte=19,
            location__place_id=["4671654"],
            phq_impact_severe_weather_air_quality_retail__stats=feature_stats,
            phq_impact_severe_weather_blizzard_retail__stats=feature_stats,
            phq_impact_severe_weather_blizzard_retail__phq_rank={"gt": 50},
            phq_impact_severe_weather_cold_wave_retail__stats=feature_stats,
            phq_impact_severe_weather_cold_wave_snow_retail__stats=feature_stats,
            phq_impact_severe_weather_cold_wave_snow_retail__phq_rank={"gt": 50},
            phq_impact_severe_weather_cold_wave_storm_retail__stats=feature_stats,
            phq_impact_severe_weather_dust_retail__stats=feature_stats,
            phq_impact_severe_weather_dust_storm_retail__stats=feature_stats,
            phq_impact_severe_weather_flood_retail__stats=feature_stats,
            phq_impact_severe_weather_heat_wave_retail__stats=feature_stats,
            phq_impact_severe_weather_hurricane_retail__stats=feature_stats,
            phq_impact_severe_weather_thunderstorm_retail__stats=feature_stats,
            phq_impact_severe_weather_tornado_retail__stats=feature_stats,
            phq_impact_severe_weather_tropical_storm_retail__stats=feature_stats,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "hour_of_day_active": {"gt": 10, "lte": 19},
                "location": {"place_id": ["4671654"]},
                "phq_impact_severe_weather_air_quality_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_blizzard_retail": {"stats": feature_stats, "phq_rank": {"gt": 50}},
                "phq_impact_severe_weather_cold_wave_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_cold_wave_snow_retail": {"stats": feature_stats, "phq_rank": {"gt": 50}},
                "phq_impact_severe_weather_cold_wave_storm_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_dust_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_dust_storm_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_flood_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_heat_wave_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_hurricane_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_thunderstorm_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_tornado_retail": {"stats": feature_stats},
                "phq_impact_severe_weather_tropical_storm_retail": {"stats": feature_stats},
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_impact_severe_weather_request_params_dicts(self, client):
        feature_criteria = {"stats": ["avg", "count", "max", "median", "min", "sum", "std_dev"], "phq_rank": {"gt": 50}}
        client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            hour_of_day_start={"gte": 10, "lt": 11},
            location={"geo": {"lon": -71.49978, "lat": 41.75038, "radius": "30km"}},
            phq_impact_severe_weather_air_quality_retail=feature_criteria,
            phq_impact_severe_weather_blizzard_retail=feature_criteria,
            phq_impact_severe_weather_cold_wave_retail=feature_criteria,
            phq_impact_severe_weather_cold_wave_snow_retail=feature_criteria,
            phq_impact_severe_weather_cold_wave_storm_retail=feature_criteria,
            phq_impact_severe_weather_dust_retail=feature_criteria,
            phq_impact_severe_weather_dust_storm_retail=feature_criteria,
            phq_impact_severe_weather_flood_retail=feature_criteria,
            phq_impact_severe_weather_heat_wave_retail=feature_criteria,
            phq_impact_severe_weather_hurricane_retail=feature_criteria,
            phq_impact_severe_weather_thunderstorm_retail=feature_criteria,
            phq_impact_severe_weather_tornado_retail=feature_criteria,
            phq_impact_severe_weather_tropical_storm_retail=feature_criteria,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "hour_of_day_start": {"gte": 10, "lt": 11},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
                "phq_impact_severe_weather_air_quality_retail": feature_criteria,
                "phq_impact_severe_weather_blizzard_retail": feature_criteria,
                "phq_impact_severe_weather_cold_wave_retail": feature_criteria,
                "phq_impact_severe_weather_cold_wave_snow_retail": feature_criteria,
                "phq_impact_severe_weather_cold_wave_storm_retail": feature_criteria,
                "phq_impact_severe_weather_dust_retail": feature_criteria,
                "phq_impact_severe_weather_dust_storm_retail": feature_criteria,
                "phq_impact_severe_weather_flood_retail": feature_criteria,
                "phq_impact_severe_weather_heat_wave_retail": feature_criteria,
                "phq_impact_severe_weather_hurricane_retail": feature_criteria,
                "phq_impact_severe_weather_thunderstorm_retail": feature_criteria,
                "phq_impact_severe_weather_tornado_retail": feature_criteria,
                "phq_impact_severe_weather_tropical_storm_retail": feature_criteria,
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_viewership_request_params_underscores(self, client):
        feature_stats = ["avg", "count", "max", "median", "min", "sum", "std_dev"]
        client.features.obtain_features(
            active__gte="2017-12-31",
            active__lte="2018-01-02",
            hour_of_day_active__gt=10,
            hour_of_day_active__lte=19,
            location__place_id=["4671654"],
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
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_viewership_request_params_underscores_without_ssl_verification(self, client):
        client.features.obtain_features(
            active__gte="2017-12-31",
            location__place_id=["4671654"],
            config__verify_ssl=False,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31"},
                "location": {"place_id": ["4671654"]},
            },
            verify=False,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
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
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_viewership_request_params_dicts_without_ssl_verification(self, client):
        client.features.obtain_features(
            active={"gte": "2017-12-31"},
            location={"geo": {"lon": -71.49978, "lat": 41.75038, "radius": "30km"}},
            config={"verify_ssl": False},
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31"},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
            },
            verify=False,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_spend_request_params_underscores(self, client):
        feature_stats = ["avg", "count", "max", "median", "min", "sum", "std_dev"]
        client.features.obtain_features(
            active__gte="2017-12-31",
            active__lte="2018-01-02",
            location__place_id=["4671654"],
            phq_spend_conferences__stats=feature_stats,
            phq_spend_expos__stats=feature_stats,
            phq_spend_sports__stats=feature_stats,
            phq_spend_community__stats=feature_stats,
            phq_spend_concerts__stats=feature_stats,
            phq_spend_festivals__stats=feature_stats,
            phq_spend_performing_arts__stats=feature_stats,
            phq_spend_conferences_accommodation__stats=feature_stats,
            phq_spend_expos_accommodation__stats=feature_stats,
            phq_spend_sports_accommodation__stats=feature_stats,
            phq_spend_community_accommodation__stats=feature_stats,
            phq_spend_concerts_accommodation__stats=feature_stats,
            phq_spend_festivals_accommodation__stats=feature_stats,
            phq_spend_performing_arts_accommodation__stats=feature_stats,
            phq_spend_conferences_hospitality__stats=feature_stats,
            phq_spend_expos_hospitality__stats=feature_stats,
            phq_spend_sports_hospitality__stats=feature_stats,
            phq_spend_community_hospitality__stats=feature_stats,
            phq_spend_concerts_hospitality__stats=feature_stats,
            phq_spend_festivals_hospitality__stats=feature_stats,
            phq_spend_performing_arts_hospitality__stats=feature_stats,
            phq_spend_conferences_transportation__stats=feature_stats,
            phq_spend_expos_transportation__stats=feature_stats,
            phq_spend_sports_transportation__stats=feature_stats,
            phq_spend_community_transportation__stats=feature_stats,
            phq_spend_concerts_transportation__stats=feature_stats,
            phq_spend_festivals_transportation__stats=feature_stats,
            phq_spend_performing_arts_transportation__stats=feature_stats,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "location": {"place_id": ["4671654"]},
                "phq_spend_conferences": {"stats": feature_stats},
                "phq_spend_expos": {"stats": feature_stats},
                "phq_spend_sports": {"stats": feature_stats},
                "phq_spend_community": {"stats": feature_stats},
                "phq_spend_concerts": {"stats": feature_stats},
                "phq_spend_festivals": {"stats": feature_stats},
                "phq_spend_performing_arts": {"stats": feature_stats},
                "phq_spend_conferences_accommodation": {"stats": feature_stats},
                "phq_spend_expos_accommodation": {"stats": feature_stats},
                "phq_spend_sports_accommodation": {"stats": feature_stats},
                "phq_spend_community_accommodation": {"stats": feature_stats},
                "phq_spend_concerts_accommodation": {"stats": feature_stats},
                "phq_spend_festivals_accommodation": {"stats": feature_stats},
                "phq_spend_performing_arts_accommodation": {"stats": feature_stats},
                "phq_spend_conferences_hospitality": {"stats": feature_stats},
                "phq_spend_expos_hospitality": {"stats": feature_stats},
                "phq_spend_sports_hospitality": {"stats": feature_stats},
                "phq_spend_community_hospitality": {"stats": feature_stats},
                "phq_spend_concerts_hospitality": {"stats": feature_stats},
                "phq_spend_festivals_hospitality": {"stats": feature_stats},
                "phq_spend_performing_arts_hospitality": {"stats": feature_stats},
                "phq_spend_conferences_transportation": {"stats": feature_stats},
                "phq_spend_expos_transportation": {"stats": feature_stats},
                "phq_spend_sports_transportation": {"stats": feature_stats},
                "phq_spend_community_transportation": {"stats": feature_stats},
                "phq_spend_concerts_transportation": {"stats": feature_stats},
                "phq_spend_festivals_transportation": {"stats": feature_stats},
                "phq_spend_performing_arts_transportation": {"stats": feature_stats},
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/features_test/test_empty_search"))
    def test_spend_request_params_dicts(self, client):
        feature_criteria = {"stats": ["avg", "count", "max", "median", "min", "sum", "std_dev"], "phq_rank": {"gt": 50}}
        client.features.obtain_features(
            active={"gte": "2017-12-31", "lte": "2018-01-02"},
            location={"geo": {"lon": -71.49978, "lat": 41.75038, "radius": "30km"}},
            phq_spend_conferences=feature_criteria,
            phq_spend_expos=feature_criteria,
            phq_spend_sports=feature_criteria,
            phq_spend_community=feature_criteria,
            phq_spend_concerts=feature_criteria,
            phq_spend_festivals=feature_criteria,
            phq_spend_performing_arts=feature_criteria,
            phq_spend_conferences_accommodation=feature_criteria,
            phq_spend_expos_accommodation=feature_criteria,
            phq_spend_sports_accommodation=feature_criteria,
            phq_spend_community_accommodation=feature_criteria,
            phq_spend_concerts_accommodation=feature_criteria,
            phq_spend_festivals_accommodation=feature_criteria,
            phq_spend_performing_arts_accommodation=feature_criteria,
            phq_spend_conferences_hospitality=feature_criteria,
            phq_spend_expos_hospitality=feature_criteria,
            phq_spend_sports_hospitality=feature_criteria,
            phq_spend_community_hospitality=feature_criteria,
            phq_spend_concerts_hospitality=feature_criteria,
            phq_spend_festivals_hospitality=feature_criteria,
            phq_spend_performing_arts_hospitality=feature_criteria,
            phq_spend_conferences_transportation=feature_criteria,
            phq_spend_expos_transportation=feature_criteria,
            phq_spend_sports_transportation=feature_criteria,
            phq_spend_community_transportation=feature_criteria,
            phq_spend_concerts_transportation=feature_criteria,
            phq_spend_festivals_transportation=feature_criteria,
            phq_spend_performing_arts_transportation=feature_criteria,
        )

        client.request.assert_called_once_with(
            "post",
            "/v1/features/",
            json={
                "active": {"gte": "2017-12-31", "lte": "2018-01-02"},
                "location": {"geo": {"lat": 41.75038, "lon": -71.49978, "radius": "30km"}},
                "phq_spend_conferences": feature_criteria,
                "phq_spend_expos": feature_criteria,
                "phq_spend_sports": feature_criteria,
                "phq_spend_community": feature_criteria,
                "phq_spend_concerts": feature_criteria,
                "phq_spend_festivals": feature_criteria,
                "phq_spend_performing_arts": feature_criteria,
                "phq_spend_conferences_accommodation": feature_criteria,
                "phq_spend_expos_accommodation": feature_criteria,
                "phq_spend_sports_accommodation": feature_criteria,
                "phq_spend_community_accommodation": feature_criteria,
                "phq_spend_concerts_accommodation": feature_criteria,
                "phq_spend_festivals_accommodation": feature_criteria,
                "phq_spend_performing_arts_accommodation": feature_criteria,
                "phq_spend_conferences_hospitality": feature_criteria,
                "phq_spend_expos_hospitality": feature_criteria,
                "phq_spend_sports_hospitality": feature_criteria,
                "phq_spend_community_hospitality": feature_criteria,
                "phq_spend_concerts_hospitality": feature_criteria,
                "phq_spend_festivals_hospitality": feature_criteria,
                "phq_spend_performing_arts_hospitality": feature_criteria,
                "phq_spend_conferences_transportation": feature_criteria,
                "phq_spend_expos_transportation": feature_criteria,
                "phq_spend_sports_transportation": feature_criteria,
                "phq_spend_community_transportation": feature_criteria,
                "phq_spend_concerts_transportation": feature_criteria,
                "phq_spend_festivals_transportation": feature_criteria,
                "phq_spend_performing_arts_transportation": feature_criteria,
            },
            verify=True,
        )

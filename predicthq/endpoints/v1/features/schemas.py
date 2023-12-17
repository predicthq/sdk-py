from datetime import date
from typing import List

from typing import Optional

from pydantic import BaseModel

from predicthq.endpoints.schemas import ResultSet


class FeatureRankLevel(BaseModel):
    rank_levels: dict


class FeatureStats(BaseModel):
    avg: Optional[float] = None
    count: Optional[int] = None
    max: Optional[float] = None
    median: Optional[float] = None
    min: Optional[float] = None
    sum: Optional[float] = None
    std_dev: Optional[float] = None


class FeatureStat(BaseModel):
    stats: FeatureStats


class Feature(BaseModel):
    class Options:
        serialize_when_none = False

    date: date
    # Attendance based features
    phq_attendance_academic_graduation: Optional[FeatureStat] = None
    phq_attendance_academic_social: Optional[FeatureStat] = None
    phq_attendance_community: Optional[FeatureStat] = None
    phq_attendance_concerts: Optional[FeatureStat] = None
    phq_attendance_conferences: Optional[FeatureStat] = None
    phq_attendance_expos: Optional[FeatureStat] = None
    phq_attendance_festivals: Optional[FeatureStat] = None
    phq_attendance_performing_arts: Optional[FeatureStat] = None
    phq_attendance_school_holidays: Optional[FeatureStat] = None
    phq_attendance_sports: Optional[FeatureStat] = None
    # Attendance based feature for accommodation vertical
    phq_attendance_community_accommodation: Optional[FeatureStat] = None
    phq_attendance_concerts_accommodation: Optional[FeatureStat] = None
    phq_attendance_conferences_accommodation: Optional[FeatureStat] = None
    phq_attendance_expos_accommodation: Optional[FeatureStat] = None
    phq_attendance_festivals_accommodation: Optional[FeatureStat] = None
    phq_attendance_performing_arts_accommodation: Optional[FeatureStat] = None
    phq_attendance_sports_accommodation: Optional[FeatureStat] = None
    # Attendance based feature for hospitality vertical
    phq_attendance_community_hospitality: Optional[FeatureStat] = None
    phq_attendance_concerts_hospitality: Optional[FeatureStat] = None
    phq_attendance_conferences_hospitality: Optional[FeatureStat] = None
    phq_attendance_expos_hospitality: Optional[FeatureStat] = None
    phq_attendance_festivals_hospitality: Optional[FeatureStat] = None
    phq_attendance_performing_arts_hospitality: Optional[FeatureStat] = None
    phq_attendance_sports_hospitality: Optional[FeatureStat] = None
    # Rank based features
    phq_rank_daylight_savings: Optional[FeatureRankLevel] = None
    phq_rank_health_warnings: Optional[FeatureRankLevel] = None
    phq_rank_observances: Optional[FeatureRankLevel] = None
    phq_rank_public_holidays: Optional[FeatureRankLevel] = None
    phq_rank_school_holidays: Optional[FeatureRankLevel] = None
    phq_rank_politics: Optional[FeatureRankLevel] = None
    phq_rank_academic_session: Optional[FeatureRankLevel] = None
    phq_rank_academic_exam: Optional[FeatureRankLevel] = None
    phq_rank_academic_holiday: Optional[FeatureRankLevel] = None
    # Impact based feature criteria
    phq_impact_severe_weather_air_quality_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_blizzard_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_cold_wave_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_cold_wave_snow_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_cold_wave_storm_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_dust_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_dust_storm_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_flood_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_heat_wave_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_hurricane_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_thunderstorm_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_tornado_retail: Optional[FeatureStat] = None
    phq_impact_severe_weather_tropical_storm_retail: Optional[FeatureStat] = None
    # Viewership based features
    phq_viewership_sports: Optional[FeatureStat] = None
    phq_viewership_sports_american_football: Optional[FeatureStat] = None
    phq_viewership_sports_american_football_ncaa_men: Optional[FeatureStat] = None
    phq_viewership_sports_american_football_nfl: Optional[FeatureStat] = None
    phq_viewership_sports_auto_racing: Optional[FeatureStat] = None
    phq_viewership_sports_auto_racing_indy_car: Optional[FeatureStat] = None
    phq_viewership_sports_auto_racing_nascar: Optional[FeatureStat] = None
    phq_viewership_sports_baseball: Optional[FeatureStat] = None
    phq_viewership_sports_baseball_mlb: Optional[FeatureStat] = None
    phq_viewership_sports_baseball_ncaa_men: Optional[FeatureStat] = None
    phq_viewership_sports_basketball: Optional[FeatureStat] = None
    phq_viewership_sports_basketball_ncaa_women: Optional[FeatureStat] = None
    phq_viewership_sports_basketball_ncaa_men: Optional[FeatureStat] = None
    phq_viewership_sports_basketball_nba: Optional[FeatureStat] = None
    phq_viewership_sports_boxing: Optional[FeatureStat] = None
    phq_viewership_sports_golf: Optional[FeatureStat] = None
    phq_viewership_sports_golf_masters: Optional[FeatureStat] = None
    phq_viewership_sports_golf_pga_championship: Optional[FeatureStat] = None
    phq_viewership_sports_golf_pga_tour: Optional[FeatureStat] = None
    phq_viewership_sports_golf_us_open: Optional[FeatureStat] = None
    phq_viewership_sports_horse_racing: Optional[FeatureStat] = None
    phq_viewership_sports_horse_racing_belmont_stakes: Optional[FeatureStat] = None
    phq_viewership_sports_horse_racing_kentucky_derby: Optional[FeatureStat] = None
    phq_viewership_sports_horse_racing_preakness_stakes: Optional[FeatureStat] = None
    phq_viewership_sports_ice_hockey: Optional[FeatureStat] = None
    phq_viewership_sports_ice_hockey_nhl: Optional[FeatureStat] = None
    phq_viewership_sports_mma: Optional[FeatureStat] = None
    phq_viewership_sports_mma_ufc: Optional[FeatureStat] = None
    phq_viewership_sports_soccer: Optional[FeatureStat] = None
    phq_viewership_sports_soccer_concacaf_champions_league: Optional[FeatureStat] = None
    phq_viewership_sports_soccer_concacaf_gold_cup: Optional[FeatureStat] = None
    phq_viewership_sports_soccer_copa_america_men: Optional[FeatureStat] = None
    phq_viewership_sports_soccer_fifa_world_cup_women: Optional[FeatureStat] = None
    phq_viewership_sports_soccer_fifa_world_cup_men: Optional[FeatureStat] = None
    phq_viewership_sports_soccer_mls: Optional[FeatureStat] = None
    phq_viewership_sports_soccer_uefa_champions_league_men: Optional[FeatureStat] = None
    phq_viewership_sports_softball: Optional[FeatureStat] = None
    phq_viewership_sports_softball_ncaa_women: Optional[FeatureStat] = None
    phq_viewership_sports_tennis: Optional[FeatureStat] = None
    phq_viewership_sports_tennis_us_open: Optional[FeatureStat] = None
    phq_viewership_sports_tennis_wimbledon: Optional[FeatureStat] = None
    # PHQ spend based feature
    phq_spend_conferences: Optional[FeatureStat] = None
    phq_spend_expos: Optional[FeatureStat] = None
    phq_spend_sports: Optional[FeatureStat] = None
    phq_spend_community: Optional[FeatureStat] = None
    phq_spend_concerts: Optional[FeatureStat] = None
    phq_spend_festivals: Optional[FeatureStat] = None
    phq_spend_performing_arts: Optional[FeatureStat] = None
    # PHQ spend accommodation based feature
    phq_spend_conferences_accommodation: Optional[FeatureStat] = None
    phq_spend_expos_accommodation: Optional[FeatureStat] = None
    phq_spend_sports_accommodation: Optional[FeatureStat] = None
    phq_spend_community_accommodation: Optional[FeatureStat] = None
    phq_spend_concerts_accommodation: Optional[FeatureStat] = None
    phq_spend_festivals_accommodation: Optional[FeatureStat] = None
    phq_spend_performing_arts_accommodation: Optional[FeatureStat] = None
    # PHQ spend hospitality based feature
    phq_spend_conferences_hospitality: Optional[FeatureStat] = None
    phq_spend_expos_hospitality: Optional[FeatureStat] = None
    phq_spend_sports_hospitality: Optional[FeatureStat] = None
    phq_spend_community_hospitality: Optional[FeatureStat] = None
    phq_spend_concerts_hospitality: Optional[FeatureStat] = None
    phq_spend_festivals_hospitality: Optional[FeatureStat] = None
    phq_spend_performing_arts_hospitality: Optional[FeatureStat] = None
    # PHQ spend transportation based feature
    phq_spend_conferences_transportation: Optional[FeatureStat] = None
    phq_spend_expos_transportation: Optional[FeatureStat] = None
    phq_spend_sports_transportation: Optional[FeatureStat] = None
    phq_spend_community_transportation: Optional[FeatureStat] = None
    phq_spend_concerts_transportation: Optional[FeatureStat] = None
    phq_spend_festivals_transportation: Optional[FeatureStat] = None
    phq_spend_performing_arts_transportation: Optional[FeatureStat] = None


class FeatureResultSet(ResultSet):
    results: List[Optional[Feature]]

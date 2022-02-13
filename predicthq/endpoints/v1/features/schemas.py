from predicthq.endpoints.schemas import (
    BooleanType,
    ConfigMixin,
    DateType,
    DateRange,
    DictType,
    FloatType,
    IntRange,
    IntType,
    ListType,
    Model,
    ModelType,
    ResultSet,
    ResultType,
    StringType,
)


class FeatureCriteria(Model):
    class Options:
        serialize_when_none = True

    stats = ListType(StringType(choices=("avg", "count", "max", "median", "min", "sum", "std_dev"), default="count"))
    phq_rank = ModelType(IntRange)


class FeatureGeoPoint(Model):
    lat = FloatType(required=True, min_value=-90.0, max_value=90.0)
    lon = FloatType(required=True, min_value=-180.0, max_value=180.0)
    radius = StringType(
        regex=r"^\d+(k?m|mi)$",
        required=True,
        messages={
            "regex": "Radius needs to define a number and unit (m, km, mi) eg. 100km",
        },
    )


class FeatureLocation(Model):
    class Options:
        serialize_when_none = False

    geo = ModelType(FeatureGeoPoint)
    place_id = ListType(StringType)


class HourOfDayRange(Model):
    class Options:
        serialize_when_none = False

    gt = IntType(min_value=0, max_value=23)
    gte = IntType(min_value=0, max_value=23)
    lt = IntType(min_value=0, max_value=23)
    lte = IntType(min_value=0, max_value=23)


class FeatureRequest(ConfigMixin, Model):
    class Options:
        serialize_when_none = False

    active = ModelType(DateRange, required=True)
    hour_of_day_active = ModelType(HourOfDayRange)
    hour_of_day_start = ModelType(HourOfDayRange)
    hour_of_day_end = ModelType(HourOfDayRange)
    location = ModelType(FeatureLocation, required=True)
    # Attendance based feature criteria
    phq_attendance_academic_graduation = ModelType(FeatureCriteria)
    phq_attendance_academic_social = ModelType(FeatureCriteria)
    phq_attendance_community = ModelType(FeatureCriteria)
    phq_attendance_concerts = ModelType(FeatureCriteria)
    phq_attendance_conferences = ModelType(FeatureCriteria)
    phq_attendance_expos = ModelType(FeatureCriteria)
    phq_attendance_festivals = ModelType(FeatureCriteria)
    phq_attendance_performing_arts = ModelType(FeatureCriteria)
    phq_attendance_sports = ModelType(FeatureCriteria)
    # Rank based feature criteria
    phq_rank_daylight_savings = BooleanType()
    phq_rank_health_warnings = BooleanType()
    phq_rank_observances = BooleanType()
    phq_rank_public_holidays = BooleanType()
    phq_rank_school_holidays = BooleanType()
    phq_rank_politics = BooleanType()
    phq_rank_academic_session = BooleanType()
    phq_rank_academic_exam = BooleanType()
    phq_rank_academic_holiday = BooleanType()
    # Viewership based feature criteria
    phq_viewership_sports = ModelType(FeatureCriteria)
    phq_viewership_sports_american_football = ModelType(FeatureCriteria)
    phq_viewership_sports_american_football_ncaa_men = ModelType(FeatureCriteria)
    phq_viewership_sports_american_football_nfl = ModelType(FeatureCriteria)
    phq_viewership_sports_auto_racing = ModelType(FeatureCriteria)
    phq_viewership_sports_auto_racing_indy_car = ModelType(FeatureCriteria)
    phq_viewership_sports_auto_racing_nascar = ModelType(FeatureCriteria)
    phq_viewership_sports_baseball = ModelType(FeatureCriteria)
    phq_viewership_sports_baseball_mlb = ModelType(FeatureCriteria)
    phq_viewership_sports_baseball_ncaa_men = ModelType(FeatureCriteria)
    phq_viewership_sports_basketball = ModelType(FeatureCriteria)
    phq_viewership_sports_basketball_ncaa_women = ModelType(FeatureCriteria)
    phq_viewership_sports_basketball_ncaa_men = ModelType(FeatureCriteria)
    phq_viewership_sports_basketball_nba = ModelType(FeatureCriteria)
    phq_viewership_sports_boxing = ModelType(FeatureCriteria)
    phq_viewership_sports_golf = ModelType(FeatureCriteria)
    phq_viewership_sports_golf_masters = ModelType(FeatureCriteria)
    phq_viewership_sports_golf_pga_championship = ModelType(FeatureCriteria)
    phq_viewership_sports_golf_pga_tour = ModelType(FeatureCriteria)
    phq_viewership_sports_golf_us_open = ModelType(FeatureCriteria)
    phq_viewership_sports_horse_racing = ModelType(FeatureCriteria)
    phq_viewership_sports_horse_racing_belmont_stakes = ModelType(FeatureCriteria)
    phq_viewership_sports_horse_racing_kentucky_derby = ModelType(FeatureCriteria)
    phq_viewership_sports_horse_racing_preakness_stakes = ModelType(FeatureCriteria)
    phq_viewership_sports_ice_hockey = ModelType(FeatureCriteria)
    phq_viewership_sports_ice_hockey_nhl = ModelType(FeatureCriteria)
    phq_viewership_sports_mma = ModelType(FeatureCriteria)
    phq_viewership_sports_mma_ufc = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer_concacaf_champions_league = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer_concacaf_gold_cup = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer_copa_america_men = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer_fifa_world_cup_women = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer_fifa_world_cup_men = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer_mls = ModelType(FeatureCriteria)
    phq_viewership_sports_soccer_uefa_champions_league_men = ModelType(FeatureCriteria)
    phq_viewership_sports_softball = ModelType(FeatureCriteria)
    phq_viewership_sports_softball_ncaa_women = ModelType(FeatureCriteria)
    phq_viewership_sports_tennis = ModelType(FeatureCriteria)
    phq_viewership_sports_tennis_us_open = ModelType(FeatureCriteria)
    phq_viewership_sports_tennis_wimbledon = ModelType(FeatureCriteria)


class FeatureRankLevel(Model):
    class Options:
        serialize_when_none = False

    rank_levels = DictType(StringType)


class FeatureStats(Model):
    class Options:
        serialize_when_none = False

    avg = FloatType()
    count = IntType()
    max = FloatType()
    median = FloatType()
    min = FloatType()
    sum = FloatType()
    std_dev = FloatType()


class FeatureStat(Model):
    class Options:
        serialize_when_none = False

    stats = ModelType(FeatureStats)


class Feature(Model):
    class Options:
        serialize_when_none = False

    date = DateType()
    # Attendance based features
    phq_attendance_academic_graduation = ModelType(FeatureStat)
    phq_attendance_academic_social = ModelType(FeatureStat)
    phq_attendance_community = ModelType(FeatureStat)
    phq_attendance_concerts = ModelType(FeatureStat)
    phq_attendance_conferences = ModelType(FeatureStat)
    phq_attendance_expos = ModelType(FeatureStat)
    phq_attendance_festivals = ModelType(FeatureStat)
    phq_attendance_performing_arts = ModelType(FeatureStat)
    phq_attendance_sports = ModelType(FeatureStat)
    # Rank based features
    phq_rank_daylight_savings = ModelType(FeatureRankLevel)
    phq_rank_health_warnings = ModelType(FeatureRankLevel)
    phq_rank_observances = ModelType(FeatureRankLevel)
    phq_rank_public_holidays = ModelType(FeatureRankLevel)
    phq_rank_school_holidays = ModelType(FeatureRankLevel)
    phq_rank_politics = ModelType(FeatureRankLevel)
    phq_rank_academic_session = ModelType(FeatureRankLevel)
    phq_rank_academic_exam = ModelType(FeatureRankLevel)
    phq_rank_academic_holiday = ModelType(FeatureRankLevel)
    # Viewership based features
    phq_viewership_sports = ModelType(FeatureStat)
    phq_viewership_sports_american_football = ModelType(FeatureStat)
    phq_viewership_sports_american_football_ncaa_men = ModelType(FeatureStat)
    phq_viewership_sports_american_football_nfl = ModelType(FeatureStat)
    phq_viewership_sports_auto_racing = ModelType(FeatureStat)
    phq_viewership_sports_auto_racing_indy_car = ModelType(FeatureStat)
    phq_viewership_sports_auto_racing_nascar = ModelType(FeatureStat)
    phq_viewership_sports_baseball = ModelType(FeatureStat)
    phq_viewership_sports_baseball_mlb = ModelType(FeatureStat)
    phq_viewership_sports_baseball_ncaa_men = ModelType(FeatureStat)
    phq_viewership_sports_basketball = ModelType(FeatureStat)
    phq_viewership_sports_basketball_ncaa_women = ModelType(FeatureStat)
    phq_viewership_sports_basketball_ncaa_men = ModelType(FeatureStat)
    phq_viewership_sports_basketball_nba = ModelType(FeatureStat)
    phq_viewership_sports_boxing = ModelType(FeatureStat)
    phq_viewership_sports_golf = ModelType(FeatureStat)
    phq_viewership_sports_golf_masters = ModelType(FeatureStat)
    phq_viewership_sports_golf_pga_championship = ModelType(FeatureStat)
    phq_viewership_sports_golf_pga_tour = ModelType(FeatureStat)
    phq_viewership_sports_golf_us_open = ModelType(FeatureStat)
    phq_viewership_sports_horse_racing = ModelType(FeatureStat)
    phq_viewership_sports_horse_racing_belmont_stakes = ModelType(FeatureStat)
    phq_viewership_sports_horse_racing_kentucky_derby = ModelType(FeatureStat)
    phq_viewership_sports_horse_racing_preakness_stakes = ModelType(FeatureStat)
    phq_viewership_sports_ice_hockey = ModelType(FeatureStat)
    phq_viewership_sports_ice_hockey_nhl = ModelType(FeatureStat)
    phq_viewership_sports_mma = ModelType(FeatureStat)
    phq_viewership_sports_mma_ufc = ModelType(FeatureStat)
    phq_viewership_sports_soccer = ModelType(FeatureStat)
    phq_viewership_sports_soccer_concacaf_champions_league = ModelType(FeatureStat)
    phq_viewership_sports_soccer_concacaf_gold_cup = ModelType(FeatureStat)
    phq_viewership_sports_soccer_copa_america_men = ModelType(FeatureStat)
    phq_viewership_sports_soccer_fifa_world_cup_women = ModelType(FeatureStat)
    phq_viewership_sports_soccer_fifa_world_cup_men = ModelType(FeatureStat)
    phq_viewership_sports_soccer_mls = ModelType(FeatureStat)
    phq_viewership_sports_soccer_uefa_champions_league_men = ModelType(FeatureStat)
    phq_viewership_sports_softball = ModelType(FeatureStat)
    phq_viewership_sports_softball_ncaa_women = ModelType(FeatureStat)
    phq_viewership_sports_tennis = ModelType(FeatureStat)
    phq_viewership_sports_tennis_us_open = ModelType(FeatureStat)
    phq_viewership_sports_tennis_wimbledon = ModelType(FeatureStat)


class FeatureResultSet(ResultSet):
    results = ResultType(Feature)

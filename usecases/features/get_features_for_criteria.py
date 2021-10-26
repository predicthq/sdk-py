from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)

# Get sport attendance and public holiday rank features in a 150km radius around the given geo point  (lat, lon)
# Do the aggregations over the period [2019-11-28 TO 2020-01-05]
# Filter the sports to only account for those events with a rank > 50
for feature in phq.features.obtain_features(
        active__gte="2019-11-28",
        active__lte="2020-01-05",
        location__geo={
            "lon": -71.49978,
            "lat": 41.62064,
            "radius": "150km"
        },
        phq_rank_public_holidays=True,
        phq_attendance_sports__stats=["count", "median"],
        phq_attendance_sports__phq_rank={
            "gt": 50
        }
):
    print(feature.date, feature.phq_attendance_sports.stats.count,
          feature.phq_rank_public_holidays.rank_levels)

# Get sport attendance and public holiday rank features across the places [Rhode Island(6295630), Spokane County(5811704), Chicago(4887398)]
# Do the aggregations over the period [2019-11-28 TO 2020-01-05]
# Filter the sports to only account for those events with a rank > 50
for feature in phq.features.obtain_features(
        active__gte="2019-11-28",
        active__lte="2020-01-05",
        location__place_id=[5224323, 5811704, 4887398],
        phq_rank_public_holidays=True,
        phq_attendance_sports__stats=["count", "median"],
        phq_attendance_sports__phq_rank={
            "gt": 50
        }
):
    print(feature.date, feature.phq_attendance_sports.stats.count,
          feature.phq_rank_public_holidays.rank_levels)

# Get viewership features across the places [Rhode Island(6295630), Spokane County(5811704), Chicago(4887398)]
# Do the aggregations over the period [2019-11-28 TO 2020-01-05]
# Using broadcasts which starts between 9am - 11am
for feature in phq.features.obtain_features(
        active__gte="2019-11-28",
        active__lte="2020-01-05",
        hour_of_day_start__gte=9,
        hour_of_day_start__lt=11,
        location__place_id=[5224323, 5811704, 4887398],
        phq_viewership_sports__stats=["count", "median"],
        phq_viewership_sports__phq_rank={
            "gt": 50
        },
        phq_viewership_sports_american_football__stats=["count", "median"],
        phq_viewership_sports_american_football__phq_rank={
            "gt": 50
        },
        phq_viewership_sports_basketball_nba__stats=["count", "median"],
        phq_viewership_sports_basketball_nba__phq_rank={
            "gt": 50
        }
):
    print(feature.date, feature.phq_viewership_sports.stats.count,
          feature.phq_viewership_sports.stats.median,
          feature.phq_viewership_sports_american_football.stats.count,
          feature.phq_viewership_sports_american_football.stats.median,
          feature.phq_viewership_sports_basketball_nba.stats.count,
          feature.phq_viewership_sports_basketball_nba.stats.median)

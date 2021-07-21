from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)

# Get sport attendnace and public holiday rank features in a 150km radius around the given geo point  (lat, lon)
# Do the aggreations over the period [2019-11-28 TO 2020-01-05]
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


# Get sport attendnace and public holiday rank features across the places [Rhode Island(6295630), Spokane County(5811704), Chicago(4887398)]
# Do the aggreations over the period [2019-11-28 TO 2020-01-05]
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

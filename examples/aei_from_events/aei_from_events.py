from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/

EVENT_ENDPOINT_COLUMNS = ['id', 'title', 'description', 'start', 'end',
       'duration', 'labels', 'category', 'timezone', 'country', 'location',
       'scope', 'rank', 'local_rank',
       'phq_attendance', 'state', 'deleted_reason', 'first_seen']

ACCESS_TOKEN = '' # USER TO INCLUDE THEIR OWN TOKEN
phq = Client(access_token=ACCESS_TOKEN)

import pandas as pd
from datetime import datetime, timedelta

# Definition: Events with a start and end date and time.
#             PredictHQ models predict attendances for each of these events.
ATTENDANCE_CATEGORIES = ['community', 'concerts', 'conferences', 'expos',
                         'festivals', 'performing-arts', 'sports']

# Definition: These are events with a start and end date, but are more fluid in
#             impact, such as observances or school holidays.
NON_ATTENDANCE_CATEGORIES = ['academic', 'daylight-savings', 'observances',
                             'politics', 'public-holidays', 'school-holidays']

# Definition: Live coverage of breaking events such as severe weather and
#             terrorism. The API updates minute to minute to ensure accuracy.
UNSCHEDULED_CATEGORIES = ['airport-delays', 'disasters', 'health-warnings',
                          'severe-weather', 'terror']

# represents the collective sum of all event categories
ALL_CATEGORIES = ATTENDANCE_CATEGORIES + NON_ATTENDANCE_CATEGORIES + UNSCHEDULED_CATEGORIES

def generate_calendar(start, end):
    """
    Generate a list of dates between a start and end period.
    """
    clean_start = str(start).split('+')[0]
    start_datetime = datetime.strptime(clean_start, '%Y-%m-%d %H:%M:%S')

    clean_end = str(end).split('+')[0]
    end_datetime = datetime.strptime(clean_end, '%Y-%m-%d %H:%M:%S')

    date_difference = end_datetime - start_datetime
    date_range = []
    for d in range(0, date_difference.days + 1):
        temp_date = start_datetime + timedelta(days=d)
        date_range.append(str(temp_date).split(' ')[0])
    return date_range

def pivot_event_impact_by_event_type(cal, events_pd):
    """Returns a dataframe with the summed impact (daily phq_attendance) across
       all categories. This dataframe imputes zeros for days with no events
       (often dependent upon the minimum PHQ rank threshold used).
    """
    all_pd = []
    for day in cal:
        d_formatted = day + 'T00:00:00Z'
        qualified_events = events_pd[(events_pd['start'] <= d_formatted) & \
                                     (events_pd['end'] >= d_formatted)]

        # Calculate the summed impact across categories at a daily granularity
        # for the filtered set of events that meet the above condition
        qualified_events_agg = (qualified_events.groupby('category')['impact']
                                                .sum().reset_index())
        qualified_events_pivot = (pd.pivot_table(qualified_events_agg,
                                                 columns = 'category',
                                                 values = 'impact',
                                                 fill_value=0))

        # append the current day to the pivoted result
        d_col = pd.DataFrame([day], columns = ['date'])
        aei_temp = pd.concat([d_col, qualified_events_pivot.reset_index(drop=True)], axis = 1)
        all_pd.append(aei_temp)
    return all_pd

def create_aggregate_event_impact(df, event_groupings = ATTENDANCE_CATEGORIES):
    """
    Provided a dataframe of events (typically pulled from the events endpoint),
    transform into a format that is easy to use for improving forecasting.

    Returns a dataframe containing the summed impact of events by event category
    per day. The method for aggregation is currently irrespective of the
    category type, so it is recommended that each of the three event
    category groupings are treated independently.
    """
    att_df = df[df.category.isin(event_groupings) == True]
    att_df['days_duration'] = [1 if x / 86400 < 1 else round(x / 86400, 0) for x in att_df.duration]
    att_df['impact'] = round(att_df.phq_attendance / att_df.days_duration, 0)
    start_cal, end_cal = att_df.start.min(), att_df.end.max()

    print(start_cal, end_cal)
    df_cal = generate_calendar(start_cal, end_cal)

    aei_pd = pd.concat(pivot_event_impact_by_event_type(df_cal, att_df), axis = 0).fillna(0)
    return aei_pd

# Example Usage
# Step 1 - Query for events
start = {
    'gte': '2019-01-01',
    'lte': '2019-01-07',
    'tz': 'America/Los_Angeles',
}

# collect a dataframe of seattle events
LOCATION_STATEMENT = '20km@47.6062,-122.3321'
seattle_query = (phq.events.search(start=start,
                                   state='active',
                                   within=LOCATION_STATEMENT,
                                   category=ATTENDANCE_CATEGORIES,
                                   rank={'gte': 30, 'lte': 100}).iter_all())

# Transform query result into a dataframe
expanded_events = [[event[column] for column in EVENT_ENDPOINT_COLUMNS] for event in [*seattle_query]]
all_seattle_events = pd.DataFrame(expanded_events, columns = EVENT_ENDPOINT_COLUMNS)

# Step 2 - Transform the events into an Aggregate Event Impact (AEI) Dataframe
seattle_aei = (create_aggregate_event_impact(all_seattle_events,
                                             event_groupings = ATTENDANCE_CATEGORIES))

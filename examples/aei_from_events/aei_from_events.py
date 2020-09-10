import pandas as pd

all_cat = ['festivals', 'school-holidays', 'airport-delays', 'sports',
           'performing-arts', 'concerts', 'public-holidays', 'community',
           'observances', 'severe-weather', 'expos', 'conferences',
           'health-warnings', 'academic', 'disasters', 'politics', 'terror']

nonattended = ['public-holidays', 'observances', 'school-holidays', 'academic']

attended = ['festivals', 'sports', 'performing-arts',
            'concerts', 'community', 'expos', 'conferences']

unscheduled = ['airport-delays', 'health-warnings', 'disasters', 'politics', 'terror', 'severe-weather']

from datetime import datetime, timedelta

def gen_cal(st, ed):
    clean_start = st.replace('T', ' ').replace('Z', '')
    start_dt = datetime.strptime(clean_start, '%Y-%m-%d %H:%M:%S')

    clean_end = ed.replace('T', ' ').replace('Z', '')
    end_dt = datetime.strptime(clean_end, '%Y-%m-%d %H:%M:%S')

    date_diff = end_dt - start_dt
    date_range = []
    for d in range(0, date_diff.days + 1):
        res = start_dt + timedelta(days=d)
        date_range.append(str(res).split(' ')[0])
    return date_range

def gen_aei_from_events(cal, events_pd):
    all_pd = []
    for d in cal:
        d_formatted = d + 'T00:00:00Z'
        qualified_events = events_pd[(events_pd['start'] <= d_formatted) & (events_pd['end'] >= d_formatted)]
        qe_agg = qualified_events.groupby('category')['impact'].sum().reset_index()
        qe_pivot = pd.pivot_table(qe_agg, columns = 'category', values = 'impact', fill_value=0)
        d_col = pd.DataFrame([d], columns = ['date'])
        aei_temp = pd.concat([d_col, qe_pivot.reset_index(drop=True)], axis = 1)
        all_pd.append(aei_temp)
    return all_pd

def attended_aei(df, event_groupings = attended):
    att_df = df[df.category.isin(event_groupings)]
    att_df['days_duration'] = [1 if x / 86400 < 1 else round(x / 86400, 0) for x in att_df.duration]
    att_df['impact'] = round(att_df.phq_attendance / att_df.days_duration, 0)
    start_cal, end_cal = att_df.start.min(), att_df.end.max()
    df_cal = gen_cal(start_cal, end_cal)

    aei_pd = pd.concat(gen_aei_from_events(df_cal, att_df), axis = 0).fillna(0)
    return aei_pd

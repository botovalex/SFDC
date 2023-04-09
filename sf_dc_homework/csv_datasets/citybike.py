import pandas as pd
from pandas.core.indexes.datetimes import date_range
bike_df = pd.read_csv('data/citibike-tripdata.csv')
""" starttime — время начала поездки (дата, время);
    stoptime — время окончания поездки (дата, время);
    start station id — идентификатор стартовой стоянки;
    start station name — название стартовой стоянки;
    start station latitude, start station longitude — географическая широта и долгота стартовой стоянки;
    end station id — идентификатор конечной стоянки;
    end station name — название конечной стоянки;
    end station latitude, end station longitude — географическая широта и долгота конечной стоянки;
    bikeid — идентификатор велосипеда;
    usertype — тип пользователя (Customer — клиент с подпиской на 24 часа или на три дня, Subscriber — подписчик с годовой арендой велосипеда);
    birth year — год рождения клиента;
    gender — пол клиента (0 — неизвестный, 1 — мужчина, 2 — женщина)."""

# print(bike_df['end station name'].value_counts())
bike_df.drop(['start station id', 'end station id'], axis=1, inplace=True)

bike_df['age'] = 2018 - bike_df['birth year']
bike_df.drop(['birth year'], axis=1, inplace=True)

bike_df['starttime'] = pd.to_datetime(bike_df['starttime'])
bike_df['stoptime'] = pd.to_datetime(bike_df['stoptime'])
bike_df['trip duration'] = bike_df['stoptime'] - bike_df['starttime']


# print(bike_df['starttime'].dt.dayofweek)
# bike_df['weekend'] = 1 if bike_df['starttime'].dt.dayofweek in [5,6] else 0
bike_df['weekend'] = bike_df['starttime'].dt.dayofweek.apply(lambda x : 1 if x==5 or x==6 else 0)
# print(bike_df['weekend'].sum())

def get_time_category(time):
    if 0 <= time <= 6:
        return 'night'
    elif 6 < time <= 12:
        return 'morning'
    elif 12 < time <= 18:
        return 'day'
    elif 18 < time <= 23:
        return 'evening'
    else:
        return 'other'
    
bike_df['time_of_day'] = bike_df['starttime'].dt.hour.apply(get_time_category)
day = bike_df[bike_df['time_of_day'] == 'day']
night = bike_df[bike_df['time_of_day'] == 'night']
print(day.shape[0] / night.shape[0])

# print(bike_df.info())
print()
import sys
sys.path.append('/anaconda3/lib/python3.7/site-packages/')

import fitbit
#import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, time

# https://dev.fitbit.com/apps/details/227XZY voor als de oauth niet meer werkt
# http://python-fitbit.readthedocs.org/


client_ID = '227XZY'
client_secret = '70c29f376516f7f1143fc601a065f57a'
ac_tkn = sys.argv[1]
rf_tkn = sys.argv[2]


authd_client = fitbit.Fitbit(client_ID, client_secret,
                             access_token=ac_tkn, refresh_token=rf_tkn)

times_list = [  'activities/minutesSedentary',
				'activities/minutesVeryActive', 
				'activities/floors',
				'activities/steps',
				'sleep/minutesAsleep',
				'sleep/awakeningsCount',
				'sleep/minutesAwake',
				'sleep/startTime',
				]


# get date from now to two years before now

now = datetime.now()
year_before = now.replace(year=now.year -1)
years_list = [str(year_before.date()), str(now.date())]

# 'activities/heart'


def grab_transform_clean(data, slice, BASE_DATE):
	data_dict = data.time_series(slice, base_date=BASE_DATE, period = '1y')
	df = pd.DataFrame()
	df = df.from_dict(data_dict[data_dict.keys()[0]])
	df = df.rename(columns={df.columns[1]:data_dict.keys()[0]})
	return df


def get_heartrate(dfheart):
	rest_heart = pd.Series([])
	for x in range(len(dfheart)):
		rh = dfheart['activities-heart'].loc[x].values()[0]
		if type(rh) != int:
			rh = rest_heart.loc[x-1]
		rest_heart.loc[x] = rh
	return rest_heart

df_years = pd.DataFrame()
for year in years_list:
	df = grab_transform_clean(authd_client,times_list[0],year)
	dfheart = grab_transform_clean(authd_client, 'activities/heart',year)
	df['RestHeart'] = get_heartrate(dfheart)
	df.dateTime=pd.to_datetime(df.dateTime)
	for x in range(1,len(times_list)):
		df_temp = grab_transform_clean(authd_client,times_list[x], year)
		df[df_temp.columns[1]] =  df_temp[df_temp.columns[1]]
	df_years = df_years.append(df)




cols = df_years.columns[df_years.dtypes.eq('object')]

for col in cols:
	if col != 'sleep-startTime':
		df_years[col] = pd.to_numeric(df_years[col], errors='coerce')

df_years.to_csv("/home/roland/wetentio/base/static/data.csv", index=False)

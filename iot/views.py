from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta, time
import pandas as pd
import os
import json
import subprocess
import sys
import numpy as np

# Create your views here.

client = boto3.client('lambda')

def fitbit_get(request):
	return render(request, 'iot/fitbit.html',{})



def fitbit_data_select_result(request):
	now = datetime.now()
	two_years_before = now.replace(year=now.year-2)
	
	if request.method == "POST":
		column_select = request.POST.get("column")
		start_date = request.POST.get("select_start")
		end_date = request.POST.get("select_end")
	else: # default waardes 
		column_select = 'activities-floors'
		start_date = str(two_years_before.date())
		end_date = str(now.date())
		
	data = pd.read_csv("/home/roland/wetentio/base/static/data.csv")
	
	data['dateTime']=pd.to_datetime(data['dateTime'], yearfirst=True)
	
	mask = (data['dateTime'] > start_date) & (data['dateTime'] <= end_date)
	data = data.loc[mask]

	
	data_select = pd.DataFrame()
	data_select['Date']= data['dateTime']
	data_select[column_select] = data[column_select]
	data_select = data_select.reset_index()
	del data_select['index']
	
	
	data_time = pd.DataFrame()
	data_time['index'] = pd.Series(data_time.index.values)
	#data_time['date'] = data['dateTime'].dt.strftime('%Y-%m-%d')
	data_time[column_select] = data[column_select]
	data_time = data_time.reset_index()
	del data_time['index']
	# remove the sleep data that has not been registered
	
	
	if column_select == 'sleep-awakeningsCount' or column_select == 'sleep-minutesAwake' or column_select == 'sleep-minutesAsleep':
		data_select = data_select.loc[data_select[column_select]!=0]
		data_select = data_select.reset_index()
		data_time = data_time.loc[data_time[column_select]!=0]
		data_time = data_time.reset_index()
		del data_select['index']
		del data_time['index']
		
	# haal de columns uit de dataset zodat hij in een dropdown menu gezet kan worden
	split_data = data.to_dict('split')
	columns = split_data['columns']
	# verwijder de columns die je niet moet kunnen selecteren zoals index en datum (die staan vooraan) 
	del columns[0:2]
	
	# zet de geselecteerde column bovenaan de lijst zodat hij in het formulier automatisch is geselecteeerd als default
	columns.remove(column_select)
	columns.insert(0, column_select)
	
	
	data_time_json = data_time.to_json(orient = 'values')
	
	#startdate = data_time['date'].iloc[0]
	#enddate = data_time['date'][len(data_time)-1]	
	
	day_group = order_by_time_agg(data_select,column_select, 'Days', 'mean')
	day_group = sort_weekdays(day_group)
	day_group_data, day_group_columns = add_index_to_data(day_group)
	day_group_data_json = json.dumps(day_group_data)
	
	month_group = order_by_time_agg(data_select,column_select,'Months', 'mean')
	month_group = sort_months(month_group)
	month_group_data, month_group_columns = add_index_to_data(month_group)
	month_group_data_json = json.dumps(month_group_data)
	
	year_group = order_by_time_agg(data_select,column_select, 'Years', 'mean')
	year_group_data, year_group_columns = add_index_to_data(year_group)
	year_group_data_json = json.dumps(year_group_data)
	
	
	
	return_dict = {'data_time': data_time_json, 
					'day_group_data':day_group_data_json ,
					'month_group_data':month_group_data_json,
					'year_group_data':year_group_data_json, 
					'column_selected':json.dumps(column_select), 
					'columns':columns, 
					'startdate':start_date,
					'enddate':end_date,
					'datacount': len(data_time) }
	
	
	#data_weekdays_json = data_weekdays.to_json(orient = 'values')
	
	return render(request, 'iot/fitbit_chart.html', return_dict )

def fitbit_time_in_bed(request):

	data = pd.read_csv("/home/roland/wetentio/base/static/data.csv")
	
	
	data_select = pd.DataFrame()
	data_select['DateStr'] = data['dateTime']
	data_select['starttime']= data['dateTime'] + ' ' + data['sleep-startTime']
	data_select['starttime'] = pd.to_datetime(data_select['starttime'])	
	data_select['minAsleep']=pd.to_timedelta(data['sleep-minutesAsleep'], unit='m')
	
	starttime = pd.Series([])
	for i in range(len(data_select)):
		row = data_select.loc[i]
		if row['starttime'].hour > 18:
			starttime.loc[i] = row['starttime'].replace(year = 2018, month = 1, day = 1)
		else:
			starttime.loc[i] = row['starttime'].replace(year = 2018, month = 1, day = 2)
	data_select['starttime'] = starttime
	
					
	
	data_select['endtime'] = data_select['starttime'] + data_select['minAsleep']
	
	data_select = data_select.dropna()
	data_select = data_select.reset_index()
	del data_select['index']
	
	
	
	
	starttime = pd.Series([])
	endtime = pd.Series([])
	for i in range(len(data_select)):
			row = data_select.loc[i]
			starttime.loc[i] = datetime.strftime(row.starttime,"new Date('%Y-%m-%dT%H:%M:%S')")
			endtime.loc[i] = datetime.strftime(row.endtime,"new Date('%Y-%m-%dT%H:%M:%S')")
	data_select['starttime'] = starttime 
	data_select['endtime'] = endtime 
	 
	del data_select['minAsleep']
		
	data_select_json = data_select.to_json(orient = 'values')
	
	data_select_json = data_select_json.replace('"new', 'new')
	data_select_json = data_select_json.replace(')"', ')')

	return render(request, 'iot/fitbit_time_in_bed.html', {'data_time_in_bed':data_select_json})
	
def hoofdpijn_get(request):
	df = pd.read_csv("/home/roland/wetentio/base/static/hoofdpijn.csv")
	df.Date=pd.to_datetime(df.Date,dayfirst=True)
	df2 = pd.DataFrame()
	df2['Date'] = pd.date_range('10/1/2013', periods=2050)
	df2['hfp'] = 0
	
	for i in range(len(df)):
		df2['hfp'].loc[df2['Date'] == df['Date'].loc[i]] = df['Intensiteit'].loc[i]
	
	
	df2.to_csv("/home/roland/wetentio/base/static/hoofdpijndata.csv", index=False)	

	return render(request, 'iot/iot_home.html', {})

def hoofdpijn_data_select_result(request):
	
	df = pd.read_csv("/home/roland/wetentio/base/static/hoofdpijn.csv")
	df.Date=pd.to_datetime(df.Date,dayfirst=True)
	
	between = pd.Series([])
	for i in range(len(df)-1):
		row = df.loc[i]
		between.loc[i]= df.Date.loc[i+1] - df.Date.loc[i]
	btw = between.dt.days
	
	btw_df = pd.DataFrame()
	#btw = btw.value_counts().sort_index()
	btw_df['btw'] = btw
	
	between_data,between_columns = add_index_to_data(btw_df)
	between_data_json = json.dumps(between_data)	

	day_group = order_by_time_agg(df, 'Intensiteit','Days')
	del day_group['Date']
	day_group = sort_weekdays(day_group)
	day_group_data, day_group_columns = add_index_to_data(day_group)
	day_group_data_json = json.dumps(day_group_data)
	
	month_group = order_by_time_agg(df,'Intensiteit','Months')
	del month_group['Date']
	month_group = sort_months(month_group)
	month_group_data, month_group_columns = add_index_to_data(month_group)
	month_group_data_json = json.dumps(month_group_data)
	
	year_group = order_by_time_agg(df,'Intensiteit','Years')
	del year_group['Date']
	year_group_data, year_group_columns = add_index_to_data(year_group)
	year_group_data_json = json.dumps(year_group_data)
	

	hoofdpijndata = pd.read_csv("/home/roland/wetentio/base/static/hoofdpijndata.csv")
	data_hoofdpijn_json = hoofdpijndata.to_json(orient = 'values')
	
	
	return render(request, 'iot/hoofdpijn_chart.html',{'day_group_data':day_group_data_json ,'month_group_data':month_group_data_json,'year_group_data':year_group_data_json, 'between_data': between_data_json})


def order_by_time_agg(dtfr, target = None, scale='Days', aggregator='count'):
	time_slicer = pd.DataFrame()
	time_slicer['Date'] = dtfr['Date']
	time_slicer[target] = dtfr[target]
	
	if scale == 'Days':
		days = pd.Series([])
		for i in range(len(time_slicer)):
			row = time_slicer.loc[i]
			days.loc[i] = datetime.strftime(row.Date, "%A") 
		time_slicer["Days"] = days
		
	elif scale == 'Months':
		months = pd.Series([])
		for i in range(len(time_slicer)):
			row = time_slicer.loc[i]
			months.loc[i] = datetime.strftime(row.Date, "%B")	
		time_slicer["Months"] = months
		
	elif scale == 'Years':
		years = pd.Series([])
		for i in range(len(time_slicer)):
			row = time_slicer.loc[i]
			years.loc[i] = datetime.strftime(row.Date, "%Y")	
		time_slicer["Years"] = years
		
	else:
		return print("""Error: scale should be: 'Days', 'Month' of 'Year' """ )
		
	
	time_scale_grouper = time_slicer.groupby([scale])
	time_scale_group = time_scale_grouper.agg([aggregator])

	return time_scale_group
	
	

def add_index_to_data(dtfr):
	split_data = dtfr.to_dict('split')
	columns = split_data['columns']
	index = split_data['index']
	data = split_data['data']
	for i in range(len(data)):
		data[i].insert(0,str(index[i]))
	return data, columns

def make_weekdays(data, column):
	data_select = pd.DataFrame()
	data_select['date'] = data['date']
	data_select['Days'] = data['Days']
	data_select[column] = data[column]
	group = data_select.groupby(['Days'])
	group = group.agg(['mean'])
	data_weekdays = sort_weekdays(group.round(2))
	return data_weekdays

def make_months(data, column):
	data_select = pd.DataFrame()
	data_select['date'] = data['date']
	data_select['Months'] = data['Months']
	data_select[column] = data[column]
	group = data_select.groupby(['Months'])
	group = group.agg(['mean'])
	data_months = sort_months(group.round(2))
	return data_months	


def sort_weekdays (dtfr):
	sorter_w = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	sorterIndex = dict(zip(sorter_w,range(len(sorter_w))))
	dtfr['Day_id'] = dtfr.index
	dtfr['Day_id'] = dtfr['Day_id'].map(sorterIndex)
	dtfr = dtfr.sort_values(by='Day_id')	
	del dtfr['Day_id']
	return dtfr
	
def sort_months(dtfr):
	sorter = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September','October','November','December']
	sorterIndex = dict(zip(sorter,range(len(sorter))))
	dtfr['Month_id'] = dtfr.index
	dtfr['Month_id'] = dtfr['Month_id'].map(sorterIndex)
	dtfr = dtfr.sort_values(by='Month_id')	
	del dtfr['Month_id']
	return dtfr

	
def fitbit_get_access(request):
	if request.method == "POST":
		code = request.POST.get("code")
	
		
	begin_systemcall = """curl -X POST -i -H 'Authorization: Basic MjI3WFpZOjcwYzI5ZjM3NjUxNmY3ZjExNDNmYzYwMWEwNjVmNTdh' -H 'Content-Type: application/x-www-form-urlencoded' -d "clientId=227XZY" -d "grant_type=authorization_code" -d "redirect_uri=http%3A%2F%2F127.0.0.1%3A8080%2F" -d "code="""
	einde_systemcall = """" https://api.fitbit.com/oauth2/token > /home/roland/wetentio/base/static/output.file"""
	code_string = begin_systemcall + code + einde_systemcall
	#os.system(code_string)
	
	try:
		retcode = subprocess.call(code_string,shell=True)
		if retcode < 0:
			print("Child was terminated by signal", -retcode, file=sys.stderr)
		else:
			print("Child returned", retcode, file=sys.stderr)
	except OSError as e:
		print("Execution failed:", e, file=sys.stderr)
		
	return render(request, 'iot/iot_home.html',{})

def fitbit_get_data(request):
	
	file = open('/home/roland/wetentio/base/static/output.file', 'r') 
	tekst = file.read()
	begin = tekst.find('access_token') -2
	eind = len(tekst)
	json_tekst = tekst[begin:eind]
	tokens = json.loads(json_tekst)
	access_token = tokens['access_token'] 
	refresh_token = tokens['refresh_token']
	
	fitbit_read_file = '/home/roland/wetentio/iot/fitbit-master/get_fitbit_data.py '
	fitbit_call = 'python2.7 '+ fitbit_read_file + access_token + ' ' + refresh_token 
	
	try:
		retcode = subprocess.call(fitbit_call, shell=True)
		if retcode < 0:
			print("Child was terminated by signal", -retcode, file=sys.stderr)
		else:
			print("Child returned", retcode, file=sys.stderr)
	except OSError as e:
		print("Execution failed:", e, file=sys.stderr)
	

	return render(request, 'iot/iot_home.html',{'python_call':retcode})
	
def iot_home(request):
	return render(request, 'iot/iot_home.html',{})
	
def iot_status(request):
	dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
	table = dynamodb.Table('TimeSeriesStratus')

	response = table.scan(
		FilterExpression=Attr('date').begins_with('2018') | Attr('date').begins_with('2019'))

	items = response['Items']

	# make the dataframe using Pandas
	data = pd.DataFrame(items)


	# make useful datetime entries 
	datetime = pd.Series([])
	for i in range(len(data)):
		row = data.loc[i]
		datetime.loc[i] = row['date'] + 'T' + row['time']
	data['datetime'] = datetime
	data['dt'] = pd.to_datetime(data['datetime'])
	del data['datetime']
	del data['time']

	# transform raw data in DynamoDB to categories in column named 'activities'

	activity = pd.Series([])
	for i in range(len(data)):
		row = data.loc[i]
		row_info = row['info']
		activity.loc[i] = row_info['value']
	data['activity'] = activity
	del data['info']

	# sort the data on time
	data = data.sort_values(by='dt')

	# tell Pandas 'activity' column is of category type
	data['activity']= data['activity'].astype('category')

	# make 1hot encoding from categories
	act_1hot = pd.get_dummies(data, columns=["activity"])
	by_date_1hot = act_1hot.groupby('date')
	sum_date = by_date_1hot.sum()
	
	# prepare data for display
	data, columns = add_index_to_data(sum_date)
	
	return render(request, 'iot/aws_read_db.html', {'data':data, 'columns':columns})


def betablock(request):
	event = """ "SINGLE" """
	response = write_to_dynamodb(request,event)
	return response
	
def feet(request):
	event = """ "DOUBLE" """
	response = write_to_dynamodb(request,event)
	return response
	
def yoga(request):
	event = """ "LONG" """
	response = write_to_dynamodb(request,event)
	return response


def write_to_dynamodb(request,event):
	start_payload = """{ 
		"serialNumber": "WETENTIO",
		"clickType":"""
	end_payload = """,
		"batteryVoltage": "nvt"
		}"""
	payload = start_payload + event + end_payload
	
	response = client.invoke(
		FunctionName="WriteBetaBlockFeet",
		InvocationType='Event',
		Payload=payload
		)
	return render(request, 'iot/aws_lambda.html', {'aws_response':response})
	


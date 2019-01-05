from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta, time
import pandas as pd

# Create your views here.

client = boto3.client('lambda')

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
	split_data = sum_date.to_dict('split')
	columns = split_data['columns']
	index = split_data['index']
	data = split_data['data']
	
	for i in range(len(data)):
		data[i].insert(0,index[i])
	
	return render(request, 'iot/aws_read_db.html', {'data':data, 'columns':columns})

def betablock(request):
	payload = """{
		"serialNumber": "WETENTIO",
		"clickType": "SINGLE",
		"batteryVoltage": "nvt"
		}"""
	response = client.invoke(
		FunctionName="WriteBetaBlockFeet",
		InvocationType='Event',
		Payload=payload
		)
	return render(request, 'iot/aws_lambda.html', {'aws_response':response})
	
def feet(request):
	payload = """{
		"serialNumber": "WETENTIO",
		"clickType": "DOUBLE",
		"batteryVoltage": "nvt"
		}"""
	response = client.invoke(
		FunctionName="WriteBetaBlockFeet",
		InvocationType='Event',
		Payload=payload
		)
	return render(request, 'iot/aws_lambda.html', {'aws_response':response})
	
def yoga(request):
	payload = """{
		"serialNumber": "WETENTIO",
		"clickType": "LONG",
		"batteryVoltage": "nvt"
		}"""
	response = client.invoke(
		FunctionName="WriteBetaBlockFeet",
		InvocationType='Event',
		Payload=payload
		)
	return render(request, 'iot/aws_lambda.html', {'aws_response':response})
	


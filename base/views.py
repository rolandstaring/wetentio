from django.shortcuts import render

# Create your views here.

def base_home(request):
	return render(request, 'base/base_home.html',{})
	
def iot(request):
	return render(request, 'iot/iot_home.html',{})
	
def market(request):
	return render(request, 'market/market_list.html',{})
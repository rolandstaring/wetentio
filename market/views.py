from django.shortcuts import render
from .models import Request

# Create your views here.

def market_list(request):
	requests = Request.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'market/market_list.html', {'requests':requests})
    
    
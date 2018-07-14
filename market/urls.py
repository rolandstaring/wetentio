from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views market_list , name='market_list'),
]

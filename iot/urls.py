from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('iot/iot_status' , views.iot_status , name='iot_status'),
    path('iot/betablock', views.betablock , name='betablock'),
    path('iot/yoga', views.yoga , name='yoga'),
    path('iot/feet', views.feet , name='feet'),
]

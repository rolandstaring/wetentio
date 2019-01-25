from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.base_home , name='base_home'),
	path('base/login/',auth_views.login, name='login'),
    path('base/logout/',auth_views.logout, name='logout'),
    path('iot',views.iot, name='iot'),
    path('market',views.market, name='market'),
    ]
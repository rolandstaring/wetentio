from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.iot_home , name='iot_home'),
    path('iot_status' , views.iot_status , name='iot_status'),
    path('betablock', views.betablock , name='betablock'),
    path('yoga', views.yoga , name='yoga'),
    path('feet', views.feet , name='feet'),
    path('hoofdpijn_get',views.hoofdpijn_get, name = 'hoofdpijn_get'),
    path('fitbit_get',views.fitbit_get, name = 'fitbit_get'),
    path('fitbit_get_data',views.fitbit_get_data, name = 'fitbit_get_data'),
    path('fitbit_get_access',views.fitbit_get_access, name = 'fitbit_get_access'),
    path('fitbit_data_select_result', views.fitbit_data_select_result, name = 'fitbit_data_select_result'),
    path('hoofdpijn_data_select_result', views.hoofdpijn_data_select_result, name = 'hoofdpijn_data_select_result'),
    path('fitbit_time_in_bed',views.fitbit_time_in_bed, name = 'fitbit_time_in_bed'),
    
]

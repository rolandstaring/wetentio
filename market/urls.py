from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('market_list/', views.market_list , name='market_list'),
    path('new/', views.market_new, name='market_new'),
    path('participant_add/<int:pk>', views.participant_add, name='participant_add'),
    path('<int:pk>',views.market_detail, name='market_detail'),
]

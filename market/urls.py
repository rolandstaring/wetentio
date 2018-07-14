from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_list , name='market_list'),
    path('market/new/', views.market_new, name='market_new'),
    path('market/<int:pk>',views.market_detail, name='market_detail'),
]

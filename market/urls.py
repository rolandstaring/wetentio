from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.market_list , name='market_list'),
    path('market/new/', views.market_new, name='market_new'),
    path('market/login/',auth_views.login, name='login'),
    path('market/logout/',auth_views.logout, name='logout'),
    path('market/participant_add/<int:pk>', views.participant_add, name='participant_add'),
    path('market/<int:pk>',views.market_detail, name='market_detail'),
]

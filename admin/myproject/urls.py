from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_api_list, name='tweet_api_list'),
    path('tweets/<int:tweet_id>/', views.tweet_api_detail, name='tweet_api_detail'),
    path('tweets/create/', views.tweet_api_create, name='tweet_api_create'),
    path('tweets/<int:tweet_id>/update/', views.tweet_api_update, name='tweet_api_update'),
    path('tweets/<int:tweet_id>/delete/', views.tweet_api_delete, name='tweet_api_delete'),

    path('register/', views.register_api, name='register_api'),
    path('search/', views.search_api, name='search_api'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('records/', views.records_list, name='records_list'),
    path('records/search/', views.search_records, name='search_records'),
    path('records/add/', views.record_create, name='record_create'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
    path('records/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('records/<int:pk>/delete/', views.record_delete, name='record_delete'),
    path('analytics/', views.analytics, name='analytics'),
    path('weather/', views.weather, name='weather'),
    path('api/trigger-fetch/', views.trigger_fetch, name='trigger_fetch'),
]

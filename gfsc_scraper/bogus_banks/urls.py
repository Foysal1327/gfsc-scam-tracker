from django.urls import path
from . import views

app_name = 'bogus_banks'

urlpatterns = [
    path('', views.item_list, name='list'),
    path('filter/', views.filter_items, name='filter'),
    path('refresh/', views.refresh_items, name='refresh'),
]
# This file defines the URL patterns for the bogus banks app.
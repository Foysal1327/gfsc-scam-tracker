from django.urls import path
from . import views

app_name = 'bogus_banks'

urlpatterns = [
    path('', views.item_list, name='list'),
    path('filter/', views.filter_items, name='filter'),
    path('refresh/', views.refresh_items, name='refresh'),
]
# The above code defines URL patterns for the bogus banks app.
# - The `item_list` view will display the list of scraped items.
# - The `filter_items` view will handle filtering of the items.
# - The `refresh_items` view will refresh the list of items.
"""
URL configuration for the opportunities app.
"""
from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.home, name='home'),
    path('opportunities/', views.OpportunityListView.as_view(), name='list'),
    path('opportunities/<slug:slug>/', views.OpportunityDetailView.as_view(), name='detail'),
    path('search/', views.search_partial, name='search'),
]

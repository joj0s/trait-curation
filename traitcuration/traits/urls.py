from . import views
from django.urls import path

urlpatterns = [
    path('', views.browse, name="browse"),
    path('<int:pk>/', views.trait_detail, name="trait_detail"),
    path('datasources/', views.datasources, name="datasources"),
    path('fetchdata/', views.fetch_data, name="fetch_data")
]

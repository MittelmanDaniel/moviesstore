from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_index, name='analytics.map'),
    path('api/regional-data/', views.get_regional_data, name='analytics.api_regional_data'),
    path('region/<str:region_code>/', views.region_detail, name='analytics.region_detail'),
]

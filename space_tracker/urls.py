from django.urls import path
from . import views


app_name = 'space_tracker'


urlpatterns = [
    path('', views.tracker_ui, name='index'),
    path('api/satellites/', views.api_satellites, name='api_satellites'),
    path('api/alerts/', views.api_alerts, name='api_alerts'),
    path('api/suggest-launch/', views.suggest_launch, name='suggest_launch'),
]

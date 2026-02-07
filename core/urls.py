from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.dashboard_stats),
    path('vehicles/', views.vehicles),
    path('update/', views.update_vehicle),
    path('accidents/', views.accidents),
    path('violations/', views.violations),
    path('congestion/', views.congestion),
    path('signals/', views.signals),
    path('dispatch/', views.dispatch),
    path('resolve/', views.resolve_accident),
]

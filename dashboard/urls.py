from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('scan/<int:scan_id>/live/', views.scan_live, name='scan_live'),
    path('scan/<int:scan_id>/results/', views.scan_results, name='scan_results'),
    path('api/scan/<int:scan_id>/status/', views.api_scan_status, name='api_scan_status'),
    path('scan/<int:scan_id>/export/', views.export_report, name='export_report'),
]

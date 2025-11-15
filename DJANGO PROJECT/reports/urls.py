from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('recommendation/<int:pk>/', views.recommendation_detail, name='recommendation_detail'),
    path('history/', views.recommendation_history, name='recommendation_history'),
    path('export/pdf/<int:pk>/', views.export_pdf, name='export_pdf'),
    path('export/csv/<int:pk>/', views.export_csv, name='export_csv'),
]


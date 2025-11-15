from django.urls import path
from . import views

app_name = 'parcels'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.parcel_list, name='parcel_list'),
    path('create/', views.parcel_create, name='parcel_create'),
    path('<int:pk>/', views.parcel_detail, name='parcel_detail'),
    path('<int:pk>/update/', views.parcel_update, name='parcel_update'),
    path('<int:pk>/delete/', views.parcel_delete, name='parcel_delete'),
    path('<int:pk>/soil-test/', views.soil_test_create, name='soil_test_create'),
    path('soil-test/<int:pk>/update/', views.soil_test_update, name='soil_test_update'),
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/create/', views.crop_create, name='crop_create'),
]


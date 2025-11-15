from django.contrib import admin
from .models import Crop, LandParcel, SoilTest


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'nitrogen_requirement', 'phosphorus_requirement', 'potassium_requirement']
    search_fields = ['name']


@admin.register(LandParcel)
class LandParcelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'location', 'area_hectares', 'crop', 'soil_type', 'created_at']
    list_filter = ['soil_type', 'crop', 'created_at']
    search_fields = ['name', 'location', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SoilTest)
class SoilTestAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'test_date', 'nitrogen_ppm', 'phosphorus_ppm', 'potassium_ppm', 'ph_level']
    list_filter = ['test_date']
    search_fields = ['parcel__name', 'parcel__user__username']


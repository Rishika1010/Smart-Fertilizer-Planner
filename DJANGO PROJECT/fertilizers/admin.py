from django.contrib import admin
from .models import FertilizerProduct, FertilizerRecommendation, RecommendationItem


@admin.register(FertilizerProduct)
class FertilizerProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'nitrogen_percent', 'phosphorus_percent', 'potassium_percent', 'price_per_unit', 'unit', 'is_active']
    list_filter = ['is_active', 'unit']
    search_fields = ['name', 'brand']


class RecommendationItemInline(admin.TabularInline):
    model = RecommendationItem
    extra = 0
    readonly_fields = ['nitrogen_contribution_kg', 'phosphorus_contribution_kg', 'potassium_contribution_kg', 'cost']


@admin.register(FertilizerRecommendation)
class FertilizerRecommendationAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'user', 'generated_at', 'status', 'estimated_total_cost']
    list_filter = ['status', 'generated_at']
    search_fields = ['parcel__name', 'user__username']
    readonly_fields = ['generated_at']
    inlines = [RecommendationItemInline]


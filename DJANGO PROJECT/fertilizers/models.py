from django.db import models
from django.contrib.auth.models import User
from parcels.models import LandParcel


class FertilizerProduct(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('ton', 'Ton'),
        ('bag', 'Bag (50kg)'),
    ]
    
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    nitrogen_percent = models.FloatField(default=0, help_text="N percentage")
    phosphorus_percent = models.FloatField(default=0, help_text="P2O5 percentage")
    potassium_percent = models.FloatField(default=0, help_text="K2O percentage")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Price per unit")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.nitrogen_percent}-{self.phosphorus_percent}-{self.potassium_percent})"

    class Meta:
        ordering = ['name']


class FertilizerRecommendation(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('finalized', 'Finalized'),
        ('applied', 'Applied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='recommendations')
    generated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Crop requirements (stored for historical reference)
    crop_nitrogen_requirement = models.FloatField(default=0)
    crop_phosphorus_requirement = models.FloatField(default=0)
    crop_potassium_requirement = models.FloatField(default=0)
    
    # Current soil status (stored for historical reference)
    soil_nitrogen_ppm = models.FloatField(default=0)
    soil_phosphorus_ppm = models.FloatField(default=0)
    soil_potassium_ppm = models.FloatField(default=0)
    soil_ph = models.FloatField(default=7.0)
    
    # Calculated nutrient needs
    nitrogen_needed_kg = models.FloatField(default=0)
    phosphorus_needed_kg = models.FloatField(default=0)
    potassium_needed_kg = models.FloatField(default=0)
    
    # Total costs
    estimated_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Recommendation for {self.parcel.name} - {self.generated_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-generated_at']


class RecommendationItem(models.Model):
    recommendation = models.ForeignKey(FertilizerRecommendation, on_delete=models.CASCADE, related_name='items')
    fertilizer = models.ForeignKey(FertilizerProduct, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Quantity needed")
    unit = models.CharField(max_length=10, default='kg')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Nutrient contribution from this item
    nitrogen_contribution_kg = models.FloatField(default=0)
    phosphorus_contribution_kg = models.FloatField(default=0)
    potassium_contribution_kg = models.FloatField(default=0)

    def __str__(self):
        return f"{self.fertilizer.name} - {self.quantity} {self.unit}"

    class Meta:
        ordering = ['recommendation', 'fertilizer']


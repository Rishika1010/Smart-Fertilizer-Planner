from django.db import models
from django.contrib.auth.models import User


class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    nitrogen_requirement = models.FloatField(default=0, help_text="kg/ha")
    phosphorus_requirement = models.FloatField(default=0, help_text="kg/ha")
    potassium_requirement = models.FloatField(default=0, help_text="kg/ha")
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LandParcel(models.Model):
    SOIL_TYPE_CHOICES = [
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('clay', 'Clay'),
        ('silty', 'Silty'),
        ('peat', 'Peat'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='land_parcels')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    area_hectares = models.FloatField(help_text="Area in hectares")
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES, default='loamy')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']


class SoilTest(models.Model):
    parcel = models.OneToOneField(LandParcel, on_delete=models.CASCADE, related_name='soil_test')
    test_date = models.DateField()
    nitrogen_ppm = models.FloatField(help_text="Nitrogen in ppm (parts per million)", default=0)
    phosphorus_ppm = models.FloatField(help_text="Phosphorus in ppm", default=0)
    potassium_ppm = models.FloatField(help_text="Potassium in ppm", default=0)
    ph_level = models.FloatField(help_text="pH level (0-14)", default=7.0)
    organic_matter_percent = models.FloatField(help_text="Organic matter percentage", default=0)
    test_report = models.FileField(upload_to='soil_tests/', blank=True, null=True)
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil Test - {self.parcel.name} ({self.test_date})"

    class Meta:
        ordering = ['-test_date']


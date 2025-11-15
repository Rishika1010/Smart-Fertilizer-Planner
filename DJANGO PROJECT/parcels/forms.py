from django import forms
from .models import LandParcel, Crop, SoilTest


class LandParcelForm(forms.ModelForm):
    class Meta:
        model = LandParcel
        fields = ['name', 'location', 'area_hectares', 'crop', 'soil_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'area_hectares': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'soil_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SoilTestForm(forms.ModelForm):
    class Meta:
        model = SoilTest
        fields = ['test_date', 'nitrogen_ppm', 'phosphorus_ppm', 'potassium_ppm', 
                  'ph_level', 'organic_matter_percent', 'test_report', 'notes']
        widgets = {
            'test_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nitrogen_ppm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'phosphorus_ppm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'potassium_ppm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'ph_level': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '14'}),
            'organic_matter_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'test_report': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.xlsx,.csv'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'description', 'nitrogen_requirement', 'phosphorus_requirement', 'potassium_requirement']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nitrogen_requirement': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'phosphorus_requirement': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'potassium_requirement': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }


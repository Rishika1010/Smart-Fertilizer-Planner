from django import forms
from .models import FertilizerProduct, FertilizerRecommendation


class FertilizerProductForm(forms.ModelForm):
    class Meta:
        model = FertilizerProduct
        fields = ['name', 'brand', 'nitrogen_percent', 'phosphorus_percent', 'potassium_percent',
                  'price_per_unit', 'unit', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'nitrogen_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'phosphorus_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'potassium_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RecommendationNoteForm(forms.ModelForm):
    class Meta:
        model = FertilizerRecommendation
        fields = ['notes', 'status']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


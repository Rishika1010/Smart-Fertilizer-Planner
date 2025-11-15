"""
Fertilizer Recommendation Engine

This module contains the logic for generating fertilizer recommendations
based on soil test data, crop requirements, and available fertilizer products.
"""

from parcels.models import LandParcel, SoilTest, Crop
from .models import FertilizerProduct, FertilizerRecommendation, RecommendationItem


def convert_ppm_to_kg_per_hectare(ppm_value, depth_cm=15, bulk_density=1.3):
    """
    Convert ppm (parts per million) to kg/ha.
    
    Assumes:
    - Soil depth: 15cm (plow layer)
    - Bulk density: 1.3 g/cm³
    - Area: 1 hectare = 10,000 m²
    
    Formula: kg/ha = ppm × bulk_density × depth × 10
    """
    return ppm_value * bulk_density * (depth_cm / 10)


def calculate_nutrient_deficit(crop_requirement, soil_content_kg_ha, area_hectares, efficiency_factor=0.5):
    """
    Calculate how much nutrient is needed.
    
    Args:
        crop_requirement: Required nutrient in kg/ha for the crop
        soil_content_kg_ha: Available nutrient in soil (kg/ha)
        area_hectares: Area of the parcel
        efficiency_factor: Fertilizer use efficiency (typically 0.4-0.6)
    
    Returns:
        Total nutrient needed in kg
    """
    deficit_per_ha = crop_requirement - soil_content_kg_ha
    
    # Only apply if deficit exists
    if deficit_per_ha <= 0:
        return 0
    
    # Account for efficiency (not all applied fertilizer is taken up)
    adjusted_deficit = deficit_per_ha / efficiency_factor
    
    return adjusted_deficit * area_hectares


def generate_recommendation(parcel_id, user, notes=''):
    """
    Generate fertilizer recommendation for a land parcel.
    
    Args:
        parcel_id: ID of the LandParcel
        user: User object
        notes: Optional notes for the recommendation
    
    Returns:
        FertilizerRecommendation object
    """
    parcel = LandParcel.objects.get(pk=parcel_id, user=user)
    
    # Check if parcel has crop and soil test
    if not parcel.crop:
        raise ValueError("Parcel must have a crop assigned")
    
    try:
        soil_test = parcel.soil_test
    except SoilTest.DoesNotExist:
        raise ValueError("Soil test data required for recommendation")
    
    crop = parcel.crop
    area_ha = parcel.area_hectares
    
    # Convert soil nutrients from ppm to kg/ha
    soil_n_kg_ha = convert_ppm_to_kg_per_hectare(soil_test.nitrogen_ppm)
    soil_p_kg_ha = convert_ppm_to_kg_per_hectare(soil_test.phosphorus_ppm)
    soil_k_kg_ha = convert_ppm_to_kg_per_hectare(soil_test.potassium_ppm)
    
    # Calculate nutrient requirements
    n_needed = calculate_nutrient_deficit(
        crop.nitrogen_requirement, 
        soil_n_kg_ha, 
        area_ha
    )
    p_needed = calculate_nutrient_deficit(
        crop.phosphorus_requirement, 
        soil_p_kg_ha, 
        area_ha
    )
    k_needed = calculate_nutrient_deficit(
        crop.potassium_requirement, 
        soil_k_kg_ha, 
        area_ha
    )
    
    # Create recommendation record
    recommendation = FertilizerRecommendation.objects.create(
        user=user,
        parcel=parcel,
        crop_nitrogen_requirement=crop.nitrogen_requirement,
        crop_phosphorus_requirement=crop.phosphorus_requirement,
        crop_potassium_requirement=crop.potassium_requirement,
        soil_nitrogen_ppm=soil_test.nitrogen_ppm,
        soil_phosphorus_ppm=soil_test.phosphorus_ppm,
        soil_potassium_ppm=soil_test.potassium_ppm,
        soil_ph=soil_test.ph_level,
        nitrogen_needed_kg=n_needed,
        phosphorus_needed_kg=p_needed,
        potassium_needed_kg=k_needed,
        notes=notes,
    )
    
    # Get available fertilizers
    fertilizers = FertilizerProduct.objects.filter(is_active=True)
    
    total_cost = 0
    
    # Generate recommendation items
    # For each nutrient, find best matching fertilizers
    items_created = []
    
    # For Nitrogen
    if n_needed > 0:
        n_fertilizers = fertilizers.filter(nitrogen_percent__gt=0).order_by('-nitrogen_percent')
        remaining_n = n_needed
        
        for fert in n_fertilizers[:3]:  # Try top 3 N fertilizers
            if remaining_n <= 0:
                break
            
            # Calculate how much fertilizer needed to provide remaining N
            n_content = fert.nitrogen_percent / 100
            if n_content > 0:
                fert_quantity_kg = remaining_n / n_content
                
                # Convert to appropriate unit
                if fert.unit == 'bag':
                    fert_quantity = fert_quantity_kg / 50  # 50kg per bag
                elif fert.unit == 'ton':
                    fert_quantity = fert_quantity_kg / 1000
                else:
                    fert_quantity = fert_quantity_kg
                
                cost = float(fert_quantity) * float(fert.price_per_unit)
                
                item = RecommendationItem.objects.create(
                    recommendation=recommendation,
                    fertilizer=fert,
                    quantity=round(fert_quantity, 2),
                    unit=fert.unit,
                    cost=cost,
                    nitrogen_contribution_kg=remaining_n if remaining_n <= n_needed else n_needed,
                )
                items_created.append(item)
                total_cost += cost
                remaining_n = 0
                break
    
    # For Phosphorus
    if p_needed > 0:
        p_fertilizers = fertilizers.filter(phosphorus_percent__gt=0).order_by('-phosphorus_percent')
        remaining_p = p_needed
        
        for fert in p_fertilizers[:3]:
            if remaining_p <= 0:
                break
            
            p_content = fert.phosphorus_percent / 100
            if p_content > 0:
                # Convert P2O5 to P (multiply by 0.436)
                p_content_actual = p_content * 0.436
                fert_quantity_kg = remaining_p / p_content_actual
                
                if fert.unit == 'bag':
                    fert_quantity = fert_quantity_kg / 50
                elif fert.unit == 'ton':
                    fert_quantity = fert_quantity_kg / 1000
                else:
                    fert_quantity = fert_quantity_kg
                
                cost = float(fert_quantity) * float(fert.price_per_unit)
                
                item = RecommendationItem.objects.create(
                    recommendation=recommendation,
                    fertilizer=fert,
                    quantity=round(fert_quantity, 2),
                    unit=fert.unit,
                    cost=cost,
                    phosphorus_contribution_kg=remaining_p if remaining_p <= p_needed else p_needed,
                )
                items_created.append(item)
                total_cost += cost
                remaining_p = 0
                break
    
    # For Potassium
    if k_needed > 0:
        k_fertilizers = fertilizers.filter(potassium_percent__gt=0).order_by('-potassium_percent')
        remaining_k = k_needed
        
        for fert in k_fertilizers[:3]:
            if remaining_k <= 0:
                break
            
            k_content = fert.potassium_percent / 100
            if k_content > 0:
                # Convert K2O to K (multiply by 0.83)
                k_content_actual = k_content * 0.83
                fert_quantity_kg = remaining_k / k_content_actual
                
                if fert.unit == 'bag':
                    fert_quantity = fert_quantity_kg / 50
                elif fert.unit == 'ton':
                    fert_quantity = fert_quantity_kg / 1000
                else:
                    fert_quantity = fert_quantity_kg
                
                cost = float(fert_quantity) * float(fert.price_per_unit)
                
                item = RecommendationItem.objects.create(
                    recommendation=recommendation,
                    fertilizer=fert,
                    quantity=round(fert_quantity, 2),
                    unit=fert.unit,
                    cost=cost,
                    potassium_contribution_kg=remaining_k if remaining_k <= k_needed else k_needed,
                )
                items_created.append(item)
                total_cost += cost
                remaining_k = 0
                break
    
    # Update recommendation total cost
    recommendation.estimated_total_cost = total_cost
    recommendation.save()
    
    return recommendation


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import FertilizerProduct, FertilizerRecommendation
from .forms import FertilizerProductForm, RecommendationNoteForm
from .recommendation_engine import generate_recommendation
from parcels.models import LandParcel


@login_required
def product_list(request):
    search_query = request.GET.get('search', '')
    products = FertilizerProduct.objects.all()
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    active_only = request.GET.get('active_only', '')
    if active_only == 'true':
        products = products.filter(is_active=True)
    
    return render(request, 'fertilizers/product_list.html', {
        'products': products,
        'search_query': search_query,
    })


@login_required
def product_create(request):
    if request.method == 'POST':
        form = FertilizerProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fertilizer product added successfully!')
            return redirect('fertilizers:product_list')
    else:
        form = FertilizerProductForm()
    return render(request, 'fertilizers/product_form.html', {'form': form, 'title': 'Add Fertilizer Product'})


@login_required
def product_update(request, pk):
    product = get_object_or_404(FertilizerProduct, pk=pk)
    if request.method == 'POST':
        form = FertilizerProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fertilizer product updated successfully!')
            return redirect('fertilizers:product_list')
    else:
        form = FertilizerProductForm(instance=product)
    return render(request, 'fertilizers/product_form.html', {'form': form, 'title': 'Edit Fertilizer Product', 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(FertilizerProduct, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Fertilizer product deleted successfully!')
        return redirect('fertilizers:product_list')
    return render(request, 'fertilizers/product_confirm_delete.html', {'product': product})


@login_required
def generate_recommendation_view(request, pk):
    parcel = get_object_or_404(LandParcel, pk=pk, user=request.user)
    
    # Check prerequisites
    if not parcel.crop:
        messages.error(request, 'Please assign a crop to this parcel first.')
        return redirect('parcels:parcel_detail', pk=pk)
    
    try:
        soil_test = parcel.soil_test
    except Exception:
        messages.error(request, 'Please upload soil test data first.')
        return redirect('parcels:parcel_detail', pk=pk)
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        try:
            recommendation = generate_recommendation(pk, request.user, notes)
            messages.success(request, 'Fertilizer recommendation generated successfully!')
            return redirect('reports:recommendation_detail', pk=recommendation.pk)
        except Exception as e:
            messages.error(request, f'Error generating recommendation: {str(e)}')
            return redirect('parcels:parcel_detail', pk=pk)
    
    return render(request, 'fertilizers/generate_recommendation.html', {'parcel': parcel})


@login_required
def recommendation_list(request):
    recommendations = FertilizerRecommendation.objects.filter(user=request.user)
    return render(request, 'fertilizers/recommendation_list.html', {'recommendations': recommendations})


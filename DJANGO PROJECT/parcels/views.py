from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LandParcel, SoilTest, Crop
from .forms import LandParcelForm, SoilTestForm, CropForm


@login_required
def dashboard(request):
    parcels = LandParcel.objects.filter(user=request.user)
    total_parcels = parcels.count()
    total_area = sum(parcel.area_hectares for parcel in parcels)
    
    # Get parcels with soil tests
    parcels_with_tests = parcels.filter(soil_test__isnull=False)
    
    context = {
        'parcels': parcels[:5],  # Show latest 5
        'total_parcels': total_parcels,
        'total_area': total_area,
        'parcels_with_tests': parcels_with_tests.count(),
    }
    return render(request, 'parcels/dashboard.html', context)


@login_required
def parcel_list(request):
    parcels = LandParcel.objects.filter(user=request.user)
    return render(request, 'parcels/parcel_list.html', {'parcels': parcels})


@login_required
def parcel_create(request):
    if request.method == 'POST':
        form = LandParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.user = request.user
            parcel.save()
            messages.success(request, 'Land parcel created successfully!')
            return redirect('parcels:parcel_detail', pk=parcel.pk)
    else:
        form = LandParcelForm()
    return render(request, 'parcels/parcel_form.html', {'form': form, 'title': 'Add Land Parcel'})


@login_required
def parcel_detail(request, pk):
    parcel = get_object_or_404(LandParcel, pk=pk, user=request.user)
    soil_test = None
    try:
        soil_test = parcel.soil_test
    except SoilTest.DoesNotExist:
        pass
    
    context = {
        'parcel': parcel,
        'soil_test': soil_test,
    }
    return render(request, 'parcels/parcel_detail.html', context)


@login_required
def parcel_update(request, pk):
    parcel = get_object_or_404(LandParcel, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LandParcelForm(request.POST, instance=parcel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Land parcel updated successfully!')
            return redirect('parcels:parcel_detail', pk=parcel.pk)
    else:
        form = LandParcelForm(instance=parcel)
    return render(request, 'parcels/parcel_form.html', {'form': form, 'title': 'Edit Land Parcel', 'parcel': parcel})


@login_required
def parcel_delete(request, pk):
    parcel = get_object_or_404(LandParcel, pk=pk, user=request.user)
    if request.method == 'POST':
        parcel.delete()
        messages.success(request, 'Land parcel deleted successfully!')
        return redirect('parcels:parcel_list')
    return render(request, 'parcels/parcel_confirm_delete.html', {'parcel': parcel})


@login_required
def soil_test_create(request, pk):
    parcel = get_object_or_404(LandParcel, pk=pk, user=request.user)
    
    # Check if soil test already exists
    try:
        soil_test = parcel.soil_test
        messages.info(request, 'Soil test already exists for this parcel. You can update it.')
        return redirect('parcels:soil_test_update', pk=soil_test.pk)
    except SoilTest.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = SoilTestForm(request.POST, request.FILES)
        if form.is_valid():
            soil_test = form.save(commit=False)
            soil_test.parcel = parcel
            soil_test.save()
            messages.success(request, 'Soil test uploaded successfully!')
            return redirect('parcels:parcel_detail', pk=parcel.pk)
    else:
        form = SoilTestForm()
    
    return render(request, 'parcels/soil_test_form.html', {'form': form, 'parcel': parcel, 'title': 'Upload Soil Test'})


@login_required
def soil_test_update(request, pk):
    soil_test = get_object_or_404(SoilTest, pk=pk, parcel__user=request.user)
    if request.method == 'POST':
        form = SoilTestForm(request.POST, request.FILES, instance=soil_test)
        if form.is_valid():
            form.save()
            messages.success(request, 'Soil test updated successfully!')
            return redirect('parcels:parcel_detail', pk=soil_test.parcel.pk)
    else:
        form = SoilTestForm(instance=soil_test)
    
    return render(request, 'parcels/soil_test_form.html', {'form': form, 'parcel': soil_test.parcel, 'title': 'Update Soil Test'})


@login_required
def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'parcels/crop_list.html', {'crops': crops})


@login_required
def crop_create(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop added successfully!')
            return redirect('parcels:crop_list')
    else:
        form = CropForm()
    return render(request, 'parcels/crop_form.html', {'form': form, 'title': 'Add Crop'})


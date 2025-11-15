from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileUpdateForm
from .models import UserProfile


def home(request):
    """Home page - redirects to dashboard if logged in, else to login"""
    if request.user.is_authenticated:
        return redirect('parcels:dashboard')
    return redirect('accounts:login')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserProfileUpdateForm(instance=request.user)
    
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)

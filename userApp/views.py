from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.

def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
        return redirect('login')
    
    else:
        form = SignupForm()
        return render(
            request,
            template_name='registration/signup.html',
            context={
                'form': form
            }
        )
        

@login_required
def userProfileView(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    
    if request.method == 'POST':
        user_form = UserForm( request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
        return redirect('profile')
    
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        return render(
            request,
            template_name="userApp/profile.html",
            context={
                "profile":profile,
                "user_form": user_form,
                "profile_form": profile_form
            }
        )
    
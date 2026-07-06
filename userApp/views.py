from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm
from django.contrib.auth.models import User
from .models import UserProfile

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
        


def userProfileView(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    
    return render(
        request,
        template_name="userApp/profile.html",
        context={
            "profile":profile
        }
    )
    
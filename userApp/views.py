from django.shortcuts import render, redirect
from .forms import SignupForm

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
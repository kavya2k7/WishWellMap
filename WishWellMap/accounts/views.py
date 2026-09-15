from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm
from wishwell.models import FlowProgress
from django.contrib.auth.decorators import login_required

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Initialize bonus points for new user
            FlowProgress.objects.create(user=user, points=10)
            
            # Log the user in with the current request
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

# wishwell/views.py (or accounts/views.py)

@login_required 
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()  # Deletes user and cascades to all their shelves, items, and memories
        return redirect('landing')
    return render(request, 'accounts/delete_account_confirm.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()  # Deletes user and cascades to all linked data
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('login')
    
    return render(request, 'accounts/delete_account_confirm.html')
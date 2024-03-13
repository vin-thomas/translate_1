from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('rreports_2:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return render(request, 'users/login.html', {'message': "Invalid Username"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("rreports_2:index")
        else:
            return render(request, 'users/login.html', {'message': "Invalid Password"})
    else:
        return render(request, 'users/login.html', {})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("rreports_2:index")#render(request, 'users/login.html', {"message": "Account created successfully"})  # Replace 'home' with the URL name of your home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def userLogout(request):
    logout(request)
    return redirect('users:login')
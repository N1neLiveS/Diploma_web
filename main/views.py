from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login


def home(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')


def welcome(request):
    return render(request, 'main/welcome.html')


def last_step(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})


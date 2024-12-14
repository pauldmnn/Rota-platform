from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Rota, Request

# Login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect superusers to the admin panel
            if user.is_superuser:
                return redirect('/admin/')
            # Redirect regular users to the dashboard
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'rota/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# User dashboard
@login_required
def index(request):
    rotas = Rota.objects.filter(user=request.user)
    return render(request, 'rota/index.html', {"rotas": rotas})

# Admin manage rota view
@login_required
def manage_rota(request):
    if not request.user.is_staff:
        return render(request, "rota/not_authorized.html")
    
    if request.method == 'POST':
        # Handle form submissions for rota management
        pass

    rotas = Rota.objects.all()
    return render(request, "rota/manage_rota.html", {"rotas": rotas})

# Staff request day view
@login_required
def request_day(request):
    if request.method == 'POST':
        requested_day = request.POST.get("requested_day")
        Request.objects.create(user=request.user, requested_day=requested_day)
        return redirect('dashboard')
    return render(request, 'rota/request_day.html')

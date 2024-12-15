from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Rota, Request
import datetime

@login_required
def index(request):
    """
    Displays the rota for the logged-in user.
    """
    rotas = Rota.objects.filter(user=request.user).order_by('date')
    return render(request, 'rota/index.html', {"rotas": rotas})

# Login view
def custom_login(request):
    """
    Handles user login.
    Superusers are redirected to the admin panel.
    Regular users are redirected to their dashboard.
    """
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
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    """
    Displays future shifts for the logged-in user.
    """
    today = datetime.date.today()
    future_shifts = Rota.objects.filter(user=request.user, date__gte=today).order_by('date')

    return render(request, "rota/dashboard.html", {"future_shifts": future_shifts})


@login_required
def completed_shifts(request):
    """
    Displays completed shifts for the logged-in user.
    """
    today = datetime.date.today()
    completed_shifts = Rota.objects.filter(user=request.user, date__lt=today).order_by('-date')

    return render(request, "rota/completed_shifts.html", {"completed_shifts": completed_shifts})


# Admin manage rota view
@login_required
def manage_rota(request):
    if not request.user.is_staff:
        return render(request, "rota/not_authorized.html")

    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        date = request.POST.get("date")
        shift_type = request.POST.get("shift_type")

        # Validate fields
        if not date:
            return render(request, "rota/manage_rota.html", {
                "rotas": Rota.objects.all(),
                "users": User.objects.all(),
                "error": "Date is required."
            })

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return render(request, "rota/manage_rota.html", {
                "rotas": Rota.objects.all(),
                "users": User.objects.all(),
                "error": "Selected user does not exist."
            })

        # Check for duplicate rota
        existing_rota = Rota.objects.filter(user=user, date=date).exists()
        if existing_rota:
            return render(request, "rota/manage_rota.html", {
                "rotas": Rota.objects.all(),
                "users": User.objects.all(),
                "error": "This user is already scheduled for this date."
            })

        # Create the rota
        Rota.objects.create(
            user=user,
            date=date,
            shift_type=shift_type
        )
        return redirect('manage_rota')

    rotas = Rota.objects.all().order_by('date')
    users = User.objects.all()
    return render(request, "rota/manage_rota.html", {"rotas": rotas, "users": users})

# Staff request day view
@login_required
def request_day(request):
    """
    Allows staff to request specific days.
    Only logged-in non-admin users can access this view.
    """
    if request.user.is_staff:  # Admins shouldn't access this view
        return redirect('manage_requests')

    if request.method == 'POST':
        requested_day = request.POST.get("requested_day")
        # Check for duplicate requests
        existing_request = Request.objects.filter(user=request.user, requested_day=requested_day).exists()
        if existing_request:
            return render(request, "rota/request_day.html", {"error": "You have already requested this day."})

        # Create the request
        Request.objects.create(user=request.user, requested_day=requested_day)
        return redirect('dashboard')

    return render(request, "rota/request_day.html")

# Admin manage requests view
@login_required
def manage_requests(request):
    """
    Allows admins to view and respond to staff requests.
    """
    if not request.user.is_staff:  # Ensure only admins access this view
        return redirect('dashboard')

    if request.method == 'POST':
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        comment = request.POST.get("comment", "")

        try:
            staff_request = Request.objects.get(id=request_id)
            if action == "approve":
                staff_request.status = "Approved"
            elif action == "refuse":
                staff_request.status = "Refused"
                staff_request.comment = comment
            staff_request.save()
        except Request.DoesNotExist:
            pass  # Handle invalid request IDs if necessary

    requests = Request.objects.filter(status="Pending").order_by('requested_day')
    return render(request, "rota/manage_requests.html", {"requests": requests})

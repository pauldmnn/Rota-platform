from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Rota, Request, User  # Replace with your actual model names


def admin_login(request):
    """
    Custom login view for the site admin page.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Ensure the user is a staff/admin
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to the custom admin dashboard
        else:
            messages.error(request, "Invalid credentials or you do not have admin access.")
    return render(request, 'rota/admin_login.html')


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    Displays the admin dashboard.
    """
    return render(request, 'rota/admin_dashboard.html')


@user_passes_test(lambda u: u.is_staff)
def admin_manage_requests(request):
    """
    View and handle day-off requests from staff.
    """
    requests = Request.objects.filter(status='Pending').order_by('-created_at')
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        admin_comment = request.POST.get("admin_comment", "")

        day_off_request = get_object_or_404(Request, id=request_id)
        if action == "approve":
            day_off_request.status = "Approved"
        elif action == "reject":
            day_off_request.status = "Rejected"
            day_off_request.admin_comment = admin_comment
        day_off_request.save()

    return render(request, 'rota/manage_requests.html', {'requests': requests})


@user_passes_test(lambda u: u.is_staff)
def admin_weekly_rota(request):
    """
    Displays the rota for the current week.
    """
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)
    rota = Rota.objects.filter(date__range=[start_of_week, end_of_week]).order_by('date', 'user')

    return render(request, 'rota/weekly_rota.html', {
        'rota': rota,
        'week_start': start_of_week,
        'week_end': end_of_week,
    })

def staff_login(request):
    """
    Custom login view for staff.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('staff_dashboard')  # Redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'rota/login.html')

    
@user_passes_test(lambda u: u.is_staff)
def update_rota(request, rota_id):
    """
    Allows the admin to update a rota entry.
    """
    rota_entry = get_object_or_404(Rota, id=rota_id)
    if request.method == "POST":
        rota_entry.shift_type = request.POST.get("shift_type", rota_entry.shift_type)
        rota_entry.start_time = request.POST.get("start_time", rota_entry.start_time)
        rota_entry.end_time = request.POST.get("end_time", rota_entry.end_time)
        rota_entry.is_updated = True
        rota_entry.save()
        messages.success(request, "Rota updated successfully.")
        return redirect('admin_weekly_rota')

    return render(request, 'rota/update_rota.html', {'rota': rota_entry})


@login_required
def staff_dashboard(request):
    """
    Displays current and future shifts for the staff.
    """
    today = timezone.now().date()
    shifts = Rota.objects.filter(user=request.user, date__gte=today).order_by('date')

    if not shifts.exists():
        messages.info(request, "No shifts have been assigned yet.")

    return render(request, 'rota/staff_dashboard.html', {'shifts': shifts})


@login_required
def completed_shifts(request):
    """
    Displays past shifts for the staff.
    """
    today = timezone.now().date()
    shifts = Rota.objects.filter(user=request.user, date__lt=today).order_by('-date')

    if not shifts.exists():
        messages.info(request, "No completed shifts available.")

    return render(request, 'rota/completed_shifts.html', {'shifts': shifts})


@login_required
def request_day_off(request):
    """
    Allows staff to request a day off.
    """
    if request.method == "POST":
        requested_date = request.POST.get("requested_date")
        comment = request.POST.get("comment", "")
        existing_request = Request.objects.filter(user=request.user, date=requested_date).exists()

        if existing_request:
            messages.error(request, "You have already requested this day off.")
        else:
            Request.objects.create(user=request.user, date=requested_date, comment=comment)
            messages.success(request, "Day-off request submitted successfully.")

    return render(request, 'rota/request_day_off.html')


def custom_logout(request):
    """
    Logs out the user and redirects to the login page.
    """
    logout(request)
    return redirect('login')

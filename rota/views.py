from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Rota, Request, User

# Check if the user is an admin
def is_admin(user):
    return user.is_staff

# Admin login view
def admin_login(request):
    """
    Handles admin login. Only staff users can log in here.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Check if user is staff
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid credentials or you are not an admin.")
    return render(request, 'rota/admin_login.html')

# Admin dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Displays the admin dashboard.
    """
    return render(request, 'rota/admin_dashboard.html')

# Admin weekly rota view
@login_required
@user_passes_test(is_admin)
def admin_weekly_rota(request):
    """
    Displays the weekly rota for staff.
    """
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    week_days = [(week_start + timedelta(days=i)) for i in range(7)]

    rota_entries = Rota.objects.filter(date__range=(week_start, week_start + timedelta(days=6)))

    # Organize rota data for the table
    rota_data = {}
    for entry in rota_entries:
        if entry.user.username not in rota_data:
            rota_data[entry.user.username] = {}
        rota_data[entry.user.username][entry.date] = {
            'shift': f"{entry.start_time.strftime('%H:%M')} - {entry.end_time.strftime('%H:%M')}",
            'is_updated': entry.is_updated,
        }

    return render(request, 'rota/admin_weekly_rota.html', {
        'week_start': week_start,
        'week_days': week_days,
        'rota_data': rota_data,
    })

# Update rota
@login_required
@user_passes_test(is_admin)
def update_rota(request, rota_id):
    """
    Allows the admin to update an existing rota entry.
    """
    rota_entry = get_object_or_404(Rota, id=rota_id)

    if request.method == 'POST':
        rota_entry.shift_type = request.POST.get('shift_type', rota_entry.shift_type)
        rota_entry.start_time = request.POST.get('start_time', rota_entry.start_time)
        rota_entry.end_time = request.POST.get('end_time', rota_entry.end_time)
        rota_entry.is_updated = True
        rota_entry.save()
        messages.success(request, 'Rota updated successfully.')
        return redirect('admin_weekly_rota')

    return render(request, 'rota/update_rota.html', {'rota_entry': rota_entry})

# Admin logout
@login_required
@user_passes_test(is_admin)
def admin_logout(request):
    """
    Logs out the admin and redirects to the admin login page.
    """
    logout(request)
    return redirect('admin_login')

# Staff dashboard
@login_required
def staff_dashboard(request):
    """
    Displays the dashboard for staff, showing current and future shifts.
    """
    today = timezone.now().date()
    shifts = Rota.objects.filter(user=request.user, date__gte=today).order_by('date')

    return render(request, 'rota/staff_dashboard.html', {'shifts': shifts})

# Staff completed shifts
@login_required
def completed_shifts(request):
    """
    Displays completed shifts for staff.
    """
    today = timezone.now().date()
    shifts = Rota.objects.filter(user=request.user, date__lt=today).order_by('-date')

    return render(request, 'rota/completed_shifts.html', {'shifts': shifts})

# Staff request day off
@login_required
def request_day_off(request):
    """
    Allows staff to request a day off.
    """
    if request.method == 'POST':
        requested_day = request.POST.get('requested_day')
        comment = request.POST.get('comment', '')

        # Create a new request
        Request.objects.create(
            user=request.user,
            requested_day=requested_day,
            comment=comment,
            status='Pending'
        )
        messages.success(request, 'Day off request submitted.')
        return redirect('staff_dashboard')

    return render(request, 'rota/request_day_off.html')

# Admin manage requests
@login_required
@user_passes_test(is_admin)
def admin_manage_requests(request):
    """
    Allows the admin to manage day off requests from staff.
    """
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        admin_comment = request.POST.get('admin_comment', '')

        day_off_request = get_object_or_404(Request, id=request_id)
        if action == 'approve':
            day_off_request.status = 'Approved'
        elif action == 'reject':
            day_off_request.status = 'Rejected'
            day_off_request.admin_comment = admin_comment
        day_off_request.save()

    requests = Request.objects.filter(status='Pending').order_by('-requested_day')
    return render(request, 'rota/admin_manage_requests.html', {'requests': requests})

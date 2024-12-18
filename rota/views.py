from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Rota, Request, User 
from django.utils.timezone import now
from .forms import RotaForm


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

            # Redirect superusers to the rota creation page
            if user.is_superuser:
                return redirect('admin_create_rota')
            else:
                return redirect('admin_dashboard')  # Redirect other staff to the admin dashboard
        else:
            messages.error(request, "Invalid credentials or you do not have admin access.")
    return render(request, 'rota/admin_login.html')

@user_passes_test(lambda u: u.is_staff)
def admin_create_rota(request):
    """
    Allows admin/superuser to create a new rota.
    """
    if request.method == "POST":
        form = RotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to dashboard after rota creation
    else:
        form = RotaForm()

    return render(request, 'rota/admin_create_rota.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    Admin dashboard displaying pending staff requests.
    """
    # Fetch all pending requests
    pending_requests = Request.objects.filter(status="Pending").order_by('-created_at')

    return render(request, 'rota/admin_dashboard.html', {
        'pending_requests': pending_requests
    })


@user_passes_test(lambda u: u.is_staff)
def admin_manage_requests(request):
    """
    Handles the approval or rejection of staff requests.
    """
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        staff_request = get_object_or_404(Request, id=request_id)

        if action == "approve":
            staff_request.status = "Approved"
            messages.success(request, f"Request for {staff_request.date} has been approved.")
        elif action == "reject":
            staff_request.status = "Rejected"
            admin_comment = request.POST.get("admin_comment", "No comment provided")
            staff_request.admin_comment = admin_comment
            messages.error(request, f"Request for {staff_request.date} has been rejected.")
        staff_request.save()

    return redirect('admin_dashboard')


@user_passes_test(lambda u: u.is_staff)
def admin_weekly_rota(request):
    """
    Displays the rota for the current week in a table format.
    """
    today = now().date()
    start_of_week = today - timezone(days=today.weekday())  # Get Monday of the current week
    end_of_week = start_of_week + timezone(days=6)         # Get Sunday of the current week

    rota_data = {}
    staff = Rota.objects.filter(date__range=[start_of_week, end_of_week]).order_by('user', 'date')

    for shift in staff:
        if shift.user not in rota_data:
            rota_data[shift.user] = [None] * 7  # Initialize list for 7 days of the week
        index = (shift.date - start_of_week).days  # Calculate day index
        rota_data[shift.user][index] = shift

    return render(request, 'rota/weekly_rota.html', {
        'rota': rota_data,
        'week_start': start_of_week,
        'week_end': end_of_week,
    })


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


def user_login(request):
    """
    Handles login for both staff/admin and regular users.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:  # Redirect admins/superusers to the admin page
                if user.is_superuser:
                    return redirect('admin_create_rota')  # Redirect to rota creation
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:  # Redirect regular users to their dashboard
                return redirect('staff_dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'rota/login.html')

@login_required
def completed_shifts(request):
    """
    Displays completed shifts for the staff member.
    Completed shifts are those with a date earlier than today.
    """
    today = now().date()
    # Filter shifts where the date is in the past and belongs to the logged-in user
    shifts = Rota.objects.filter(user=request.user, date__lt=today).order_by('-date')

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

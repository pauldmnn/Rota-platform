from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, Rota
import datetime
from datetime import timedelta
from django.contrib import messages


def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'rota/admin_dashboard.html')


@login_required
@user_passes_test(is_admin)
def admin_weekly_rota(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    week_days = [(week_start + timedelta(days=i)) for i in range(7)]

    rota_entries = Rota.objects.filter(date__range=(week_start, week_start + timedelta(days=6)))

    # Organize rota data into a structured format
    rota_data = {}
    for entry in rota_entries:
        if entry.user.username not in rota_data:
            rota_data[entry.user.username] = {}
        rota_data[entry.user.username][entry.date] = {
            'shift': f"{entry.start_time} - {entry.end_time}",
            'is_updated': entry.is_updated,
        }

    return render(request, 'rota/admin_weekly_rota.html', {
        'week_start': week_start,
        'week_days': week_days,
        'rota_data': rota_data,
    })


@login_required
@user_passes_test(is_admin)
def update_rota(request, rota_id):
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



@login_required
def admin_weekly_rota(request):
    """
    View to display the weekly rota in a table format.
    """
    # Calculate the current week's start date (week commencing)
    today = datetime.date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday as start of the week
    week_days = [(week_start + timedelta(days=i)) for i in range(7)]  # 7 days of the week

    # Query all rota entries for this week
    rota_entries = Rota.objects.filter(date__range=(week_start, week_start + timedelta(days=6)))

    # Organize data
    rota_data = {}
    for entry in rota_entries:
        if entry.user.username not in rota_data:
            rota_data[entry.user.username] = {}
        rota_data[entry.user.username][entry.date] = f"{entry.start_time.strftime('%H:%M')} - {entry.end_time.strftime('%H:%M')}"

    # Pass data to the template
    context = {
        'week_start': week_start,
        'week_days': week_days,
        'rota_data': rota_data,
    }
    return render(request, 'rota/admin_weekly_rota.html', context)


# Login View
class AdminRedirectLoginView(auth_views.LoginView):
    """
    Custom login view that redirects admin users to the Django Admin dashboard.
    Regular users are redirected to their dashboard.
    """
    template_name = 'rota/login.html' 

    def get_success_url(self):
        """
        Redirect superusers or staff to the admin dashboard.
        Regular users go to the staff dashboard.
        """
        if self.request.user.is_superuser or self.request.user.is_staff:
            return reverse_lazy('admin:index')  
        return reverse_lazy('staff_dashboard')  


@login_required
def staff_dashboard(request):
    """
    Staff dashboard: Cane view their shifts.
    """
    today = datetime.date.today()

    shifts = Rota.objects.filter(user=request.user, date__gte=today).order_by('date')

    # Handle form submission for requesting a day off
    if request.method == "POST":
        requested_day = request.POST.get("requested_day")
        comment = request.POST.get("comment", "").strip()

        if not requested_day:
            return render(request, 'rota/staff_dashboard.html', {
                'error': "Please select a day to request off."
            })

        Request.objects.create(
            user=request.user,
            requested_day=requested_day,
            comment=comment
        )
        return redirect('staff_dashboard')

    requests = Request.objects.filter(user=request.user).order_by('-requested_day')

    return render(request, 'rota/staff_dashboard.html', {
        'shifts': shifts,
        'requests': requests
    })

@login_required
def completed_shifts(request):
    """
    Staff can view their previous worked shifts
    """
    today = datetime.date.today()

    shifts = Rota.objects.filter(user=request.user, date__lt=today).order_by('-date')

    return render(request, 'rota/completed_shifts.html', {
        'shifts': shifts
    })


@login_required
def admin_staff_requests(request):
    """
    The admin can view pending requests 
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('staff_dashboard') 

    staff_requests = Request.objects.filter(status='Pending').order_by('-requested_day')

    if request.method == "POST":
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        admin_comment = request.POST.get('admin_comment', '')

        req = Request.objects.get(id=request_id)
        if action == "approve":
            req.status = "Approved"
        elif action == "reject":
            req.status = "Rejected"
            req.admin_comment = admin_comment
        req.save()

        return redirect('admin_staff_requests')

    return render(request, 'rota/admin_staff_requests.html', {
        'staff_requests': staff_requests
    })


@login_required
def add_rota(request):
    """
    When the rota is created cannot have the same staff twice for the same date.
    """
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        date = request.POST.get("date")
        shift_type = request.POST.get("shift_type")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        try:
            Rota.objects.create(
                user_id=user_id,
                date=date,
                shift_type=shift_type,
                start_time=start_time,
                end_time=end_time,
            )
            messages.success(request, "Rota successfully added.")
            return redirect('add_rota')

        except IntegrityError:
            messages.error(request, "This staff member already has a shift for this date.")
            return redirect('add_rota')

    return render(request, 'rota/add_rota.html')

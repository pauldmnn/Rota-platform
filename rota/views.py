from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import Request, Rota
import datetime

# Custom Login View
class AdminRedirectLoginView(auth_views.LoginView):
    """
    Custom login view that redirects admin users to the Django Admin dashboard.
    Regular users are redirected to their dashboard.
    """
    template_name = 'rota/login.html'  # Path to the login template

    def get_success_url(self):
        """
        Redirect superusers or staff to the admin dashboard.
        Regular users go to the staff dashboard.
        """
        if self.request.user.is_superuser or self.request.user.is_staff:
            return reverse_lazy('admin:index')  # Redirect admin to Django Admin
        return reverse_lazy('staff_dashboard')  # Redirect regular users


@login_required
def staff_dashboard(request):
    """
    Staff dashboard: View current/future shifts and request days off.
    """
    today = datetime.date.today()

    shifts = Rota.objects.filter(user=request.user, date__gte=today).order_by('date')

    # Handle form submission for requesting a day off
    if request.method == "POST":
        requested_day = request.POST.get("requested_day")
        comment = request.POST.get("comment", "").strip()

        # Validate input
        if not requested_day:
            return render(request, 'rota/staff_dashboard.html', {
                'error': "Please select a day to request off."
            })

        # Save the request
        Request.objects.create(
            user=request.user,
            requested_day=requested_day,
            comment=comment
        )
        return redirect('staff_dashboard')

    # Fetch existing requests
    requests = Request.objects.filter(user=request.user).order_by('-requested_day')

    return render(request, 'rota/staff_dashboard.html', {
        'shifts': shifts,
        'requests': requests
    })

@login_required
def completed_shifts(request):
    """
    View to display completed shifts (past shifts) for the logged-in user.
    """
    today = datetime.date.today()

    # Fetch past shifts for the logged-in user
    shifts = Rota.objects.filter(user=request.user, date__lt=today).order_by('-date')

    return render(request, 'rota/completed_shifts.html', {
        'shifts': shifts
    })


@login_required
def admin_staff_requests(request):
    """
    Admin view to see all pending staff requests.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('staff_dashboard')  # Non-admins are redirected to their dashboard

    # Fetch all pending requests
    staff_requests = Request.objects.filter(status='Pending').order_by('-requested_day')

    if request.method == "POST":
        # Process admin approval/rejection of requests
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
    View to add a new rota entry for staff members.
    """
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        date = request.POST.get("date")
        shift_type = request.POST.get("shift_type")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        try:
            # Attempt to create the rota
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
            # Handle duplicate staff on the same date
            messages.error(request, "This staff member already has a shift for this date.")
            return redirect('add_rota')

    return render(request, 'rota/add_rota.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Rota, Request, User 
from django.utils.timezone import now, timedelta
from .forms import RotaForm, RequestForm, StaffCreationForm, StaffProfileForm
from .models import StaffProfile



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
def create_staff_profile(request):
    """
    Allows only the admin to create a staff profile.
    """
    if request.method == "POST":
        user_form = StaffCreationForm(request.POST)
        profile_form = StaffProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Save profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, f"Profile for {user.username} created successfully!")
            return redirect('admin_dashboard')  # Adjust to your admin page
    else:
        user_form = StaffCreationForm()
        profile_form = StaffProfileForm()

    return render(request, 'rota/create_staff_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def view_staff_profile(request):
    """
    Allows staff to view their profile details.
    """
    profile = get_object_or_404(StaffProfile, user=request.user)  # Use get_object_or_404 to handle missing profiles

    return render(request, 'rota/view_staff_profile.html', {
        'profile': profile
    })


@user_passes_test(lambda u: u.is_staff)
def admin_create_rota(request):
    """
    Allows admin/superuser to create a new rota.
    """
    if request.method == "POST":
        form = RotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rota created successfully!")
            return redirect('admin_dashboard')  # Redirect to dashboard after rota creation
    else:
        form = RotaForm()

    return render(request, 'rota/admin_create_rota.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    Admin dashboard displaying all pending staff requests.
    """
    # Fetch all pending requests
    staff_requests = Request.objects.filter(status='Pending').order_by('-created_at')

    return render(request, 'rota/admin_dashboard.html', {
        'staff_requests': staff_requests
    })


@user_passes_test(lambda u: u.is_staff)
def admin_manage_requests(request):
    """
    Handles approval or rejection of staff requests.
    """
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        staff_request = get_object_or_404(Request, id=request_id)

        if action == "approve":
            staff_request.status = "Approved"
            staff_request.admin_comment = "Your request has been approved."
        elif action == "reject":
            staff_request.status = "Rejected"
            staff_request.admin_comment = request.POST.get("admin_comment", "Your request has been rejected.")

        staff_request.save()

        # Add a feedback message for the user
        messages.add_message(request, messages.SUCCESS, f"Request reply has been sent to {staff_request.user.username}.")

    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_staff)
def weekly_rota(request):
    """
    View to display the weekly rota for all staff.
    """
    # Get the current week's starting date (Monday)
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
    end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week

    # Generate a list of days in the current week
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Filter rota entries for the current week
    weekly_rotas = Rota.objects.filter(date__range=[start_of_week, end_of_week]).order_by('user', 'date')

    # Organize rota entries into a list of dictionaries
    rota_by_staff = []
    for rota in weekly_rotas:
        rota_by_staff.append({
            'user': rota.user,
            'date': rota.date,
            'shift_type': rota.shift_type,
            'start_time': rota.start_time,
            'end_time': rota.end_time,
        })

    return render(request, 'rota/weekly_rota.html', {
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'week_dates': week_dates,  # Pass week dates to the template
        'rota_by_staff': rota_by_staff,
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
def staff_profile(request):
    """
    Displays the staff profile with request replies and other details.
    """
    user_requests = Request.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'rota/staff_profile.html', {
        'user_requests': user_requests
    })

def custom_logout(request):
    """
    Logs out the user and redirects to the login page.
    """
    logout(request)
    return redirect('login')


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
    Admins are restricted from accessing this view.
    """
    if request.user.is_staff:
        return redirect('admin_dashboard')  # Redirect admins to their dashboard

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            request_obj.save()
            messages.success(request, "Your request has been submitted successfully.")
            return redirect('staff_dashboard')
    else:
        form = RequestForm()

    return render(request, 'rota/request_day_off.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def create_staff_profile(request):
    """
    Allows admin to create a staff profile.
    """
    if request.method == "POST":
        user_form = StaffCreationForm(request.POST)
        profile_form = StaffProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_staff = user_form.cleaned_data['is_staff']  # Set admin rights
            user.save()

            # Update profile fields if a profile already exists
            profile = user.profile  # Access the automatically created profile
            profile_form = StaffProfileForm(request.POST, instance=profile)
            profile_form.save()

            messages.success(request, f"Profile for {user.username} created successfully!")
            return redirect('list_user_profiles')
    else:
        user_form = StaffCreationForm()
        profile_form = StaffProfileForm()

    return render(request, 'rota/create_staff_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@user_passes_test(lambda u: u.is_staff)
def list_user_profiles(request):
    """
    View for the admin to list all user profiles.
    """
    users = User.objects.all().order_by('username')
    return render(request, 'rota/list_user_profiles.html', {'users': users})


@user_passes_test(lambda u: u.is_staff)
def edit_user_profile(request, user_id):
    """
    View for the admin to edit a user's profile.
    """
    user = get_object_or_404(User, id=user_id)
    profile = user.profile  # Access the related StaffProfile

    if request.method == "POST":
        user_form = StaffCreationForm(request.POST, instance=user)
        profile_form = StaffProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Profile for {user.username} updated successfully!")
            return redirect('list_user_profiles')
    else:
        user_form = StaffCreationForm(instance=user)
        profile_form = StaffProfileForm(instance=profile)

    return render(request, 'rota/edit_user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'username': user.username,
    })


@user_passes_test(lambda u: u.is_staff)
def delete_user_profile(request, user_id):
    """
    Allows admin to delete a user profile.
    """
    user = get_object_or_404(User, id=user_id)
    if user.is_staff:
        messages.error(request, "You cannot delete another admin.")
    else:
        user.delete()
        messages.success(request, f"User {user.username} and their profile have been deleted successfully.")
    return redirect('list_user_profiles')


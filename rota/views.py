from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Rota, Request, User 
from django.utils.timezone import now, timedelta
from .forms import RotaForm, RequestForm, StaffCreationForm, StaffProfileForm
from .models import StaffProfile
from django.http import JsonResponse




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
            return redirect('admin_create_rota') 
    else:
        form = RotaForm()

    return render(request, 'rota/admin_create_rota.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def admin_allocated_shifts(request):
    """
    Displays shifts allocated to the logged-in admin.
    """
    today = timezone.now().date()
    shifts = Rota.objects.filter(user=request.user, date__gte=today).order_by('date')

    return render(request, 'rota/admin_allocated_shifts.html', {'shifts': shifts})

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
def weekly_rotas(request):
    today = now().date()

    # Define week start and end for current and next two weeks
    weeks = []
    for week_offset in range(3):
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)
        weeks.append((start_of_week, end_of_week))

    # Fetch all staff (non-superuser users for staff, adjust if needed)
    all_staff = User.objects.filter(is_active=True).order_by('first_name')

    # Fetch rotas for the three weeks
    rotas_by_week = []
    for start_of_week, end_of_week in weeks:
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        weekly_rotas = Rota.objects.filter(date__range=[start_of_week, end_of_week]).order_by('date')

        rota_by_staff = []
        for staff in all_staff:
            staff_data = {'user': staff, 'shifts': {}}
            for date in week_dates:
                staff_data['shifts'][date] = None  # Initialize with no shifts
            for rota in weekly_rotas.filter(user=staff):
                staff_data['shifts'][rota.date] = rota
            rota_by_staff.append(staff_data)

        rotas_by_week.append({
            'week_dates': week_dates,  # Ensure exactly 7 days
            'rota_by_staff': rota_by_staff,
            'start_of_week': start_of_week,
            'end_of_week': end_of_week,
        })

    return render(request, 'rota/weekly_rotas.html', {
        'rotas_by_week': rotas_by_week,
        'highlight_shift_types': ["Sickness/Absence"],  # Pass this list to the template
    })


@user_passes_test(lambda u: u.is_staff)
def update_rota_inline(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)

        user_id = data.get("user_id")
        date = data.get("date")
        shift_type = data.get("shift_type")
        sickness_or_absence_type = data.get("sickness_or_absence_type", "")

        try:
            user = get_object_or_404(User, id=user_id)
            rota, created = Rota.objects.get_or_create(user=user, date=date)

            if shift_type == "":
                rota.delete()
                return JsonResponse({'status': 'success', 'message': 'Shift removed.'})

            rota.shift_type = shift_type
            rota.sickness_or_absence_type = sickness_or_absence_type if shift_type == "Sickness/Absence" else ""
            rota.is_updated = True if shift_type == "Sickness/Absence" else False
            rota.save()

            return JsonResponse({'status': 'success', 'message': 'Shift updated.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

   
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
    Custom login view to handle user authentication.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:  # Redirect admin to admin dashboard
                return redirect('admin_dashboard')
            else:  # Redirect regular users to staff dashboard
                return redirect('staff_dashboard')
        else:
            # Check if the username exists to distinguish between wrong username and wrong password
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                messages.error(request, "Wrong password. Please try again.")
            else:
                messages.error(request, "Username not found. Please try again.")

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


def password_reset_request(request):
    """
    Displays a message instructing users to contact their manager for password assistance.
    """
    message = "Please see your line manager to reset your password."
    return render(request, "rota/password_reset_request.html", {"message": message})


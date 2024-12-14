from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from django.contrib.auth.forms import AuthenticationForm
from .models import Rota, Request

# Create your views here.
def index(request):
    rota = Rota.objects.filter(user=request.user)
    return render(request, "rota/index.html", {"rota": rota,})


@login_required
def manage_rota(request):
    if not request.user.is_staff:
        return redirect("index")

    
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        day = request.POST.get("day")
        shift_type = request.POST.get("shift_type")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        user = User.objects.get(id=user_id)
        Rota.object.update_or_create(
            user=user,
            day=day,
            default={"shift_type": shift_type, "start_time": start_time, "end_time": end_time},
        )
        return redirect("manage_rota")
    
    rota = Rota.objects.all()
    user = User.objects.all()
    return render(request, "rota/manage_rota.html", {"roat": rota, "users": users})


@login_required
def request_day(request):
    if request.method == "POST":
        requested_day = request.POST.get("requested_day")
        Request.objects.create(user=request.user, requested_day=requested_day)
        return redirect("index")
    return render(request, "rota/request_day.html")


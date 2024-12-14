from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rota, Request

# Create your views here.
def index(request):
    rota = Rota.objects.filter(user=request.user)
    return render(request, "rota/index.html", {"rota": rota,})


@login_required  # Ensure only logged-in users can access this view
def index(request):
    rotas = Rota.objects.filter(user=request.user)  # Fetch rotas for the logged-in user
    return render(request, "rota/index.html", {"rotas": rotas})

@login_required
def manage_rota(request):
    if not request.user.is_staff:
        return render(request, "rota/not_authorized.html")
    if request.method == "POST":
        # Process rota form submissions
        pass
    rotas = Rota.objects.all()
    return render(request, "rota/manage_rota.html", {"rotas": rotas})


@login_required
def request_day(request):
    if request.method == "POST":
        requested_day = request.POST.get("requested_day")
        Request.objects.create(user=request.user, requested_day=requested_day)
        return redirect("index")
    return render(request, "rota/request_day.html")


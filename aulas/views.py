from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Aula, Reserva
from .forms import ReservaForm

def home(request):
    aulas = Aula.objects.all()
    reservas = Reserva.objects.all()
    return render(request, 'home.html', {'aulas': aulas, 'reservas': reservas})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def reservar_aula(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            return redirect('home')
    else:
        form = ReservaForm()
    return render(request, 'reserva_form.html', {'form': form})

def reservas_json(request):
    eventos = []
    for reserva in Reserva.objects.all():
        eventos.append({
            "title": f"{reserva.aula.nombre} - {reserva.usuario.username}",
            "start": f"{reserva.fecha}T{reserva.hora_inicio}",
            "end": f"{reserva.fecha}T{reserva.hora_fin}",
        })
    return JsonResponse(eventos, safe=False)


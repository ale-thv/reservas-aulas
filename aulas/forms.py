from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['aula', 'curso', 'fecha', 'hora_inicio', 'hora_fin']


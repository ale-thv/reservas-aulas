from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils.timezone import datetime

class Aula(models.Model):
    TIPO_CHOICES = [
        ('laboratorio', 'Laboratorio'),
        ('salon', 'Salón Normal'),
        ('auditorio', 'Auditorio'),
    ]

    nombre = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='salon')

    def __str__(self):
        return f"{self.nombre} - Capacidad: {self.capacidad} - Tipo: {self.get_tipo_display()}"


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Reserva(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def clean(self):
        # Buscar reservas existentes en el mismo aula y fecha
        reservas_existentes = Reserva.objects.filter(
            aula=self.aula,
            fecha=self.fecha
        ).exclude(id=self.id)  # Excluirse a sí misma en caso de edición

        for reserva in reservas_existentes:
            if (
                self.hora_inicio < reserva.hora_fin and
                self.hora_fin > reserva.hora_inicio
            ):
                raise ValidationError("Ya existe una reserva que se solapa con este horario en el aula seleccionada.")

    def __str__(self):
        return f"Reserva de {self.aula.nombre} por {self.usuario.username} el {self.fecha}"

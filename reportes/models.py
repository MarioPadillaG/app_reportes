from django.db import models
from django.contrib.auth.models import User # Importante para la relación

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Reporte(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PROCESO', 'En proceso'), # Cambié a PROCESO para que coincida con tu vista
        ('RESUELTO', 'Resuelto'),
    ]

    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    lugar_especifico = models.CharField(max_length=200)
    
    # RELACIÓN CON EL USUARIO (La que faltaba)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mis_reportes")
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='MEDIA')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
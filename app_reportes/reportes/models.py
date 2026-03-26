from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): return self.nombre

class Reporte(models.Model):
    ESTADOS = [('PENDIENTE', 'Pendiente'), ('PROCESO', 'En Proceso'), ('RESUELTO', 'Resuelto')]
    
    titulo = models.CharField(max_length=200, verbose_name="Título del fallo")
    descripcion = models.TextField(verbose_name="Descripción")
    lugar_especifico = models.CharField(max_length=200, verbose_name="¿Dónde es?")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mis_reportes")

    def __str__(self): return f"{self.titulo} - {self.lugar_especifico}"
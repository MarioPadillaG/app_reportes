from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Para proteger las vistas
from django.contrib.auth.forms import UserCreationForm # Para el registro
from django.contrib import messages # Para mostrar avisos de "Éxito"
from .models import Reporte
from .forms import ReporteForm, RegistroForm

# --- VISTA DE REGISTRO (La que te faltaba) ---
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST) # USAR TU FORMULARIO PERSONALIZADO
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada con éxito! Ya puedes entrar con tu correo.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'reportes/registro.html', {'form': form})

@login_required
def lista_reportes(request):
    reportes = Reporte.objects.filter(usuario=request.user).order_by('estado', '-fecha_creacion')
    return render(request, 'reportes/lista_reportes.html', {'reportes': reportes})

@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user # Asignamos el reporte al usuario actual
            reporte.save()
            messages.success(request, 'Reporte enviado con éxito.')
            return redirect('lista_reportes')
    else:
        form = ReporteForm()
    return render(request, 'reportes/crear_reporte.html', {'form': form})

@login_required
def editar_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ReporteForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reporte actualizado.')
            return redirect('lista_reportes')
    else:
        form = ReporteForm(instance=reporte)
    return render(request, 'reportes/crear_reporte.html', {'form': form, 'editando': True})

@login_required
def eliminar_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk, usuario=request.user)
    reporte.delete()
    messages.warning(request, 'Reporte eliminado.')
    return redirect('lista_reportes')

@login_required
def cambiar_estado(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    
    # Ajusté los nombres para que coincidan con tus modelos anteriores
    if reporte.estado == "PENDIENTE":
        reporte.estado = "PROCESO"
    elif reporte.estado == "PROCESO":
        reporte.estado = "RESUELTO"
    else:
        reporte.estado = "PENDIENTE"

    reporte.save()
    return redirect('lista_reportes')
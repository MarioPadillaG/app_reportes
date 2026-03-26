from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ReporteForm
from .models import Reporte

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'reportes/registro.html', {'form': form})

@login_required
def lista_reportes(request):
    reportes = request.user.mis_reportes.all().order_by('-fecha_creacion')
    return render(request, 'reportes/lista_reportes.html', {'reportes': reportes})

@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, 'Reporte creado con éxito.')
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
    if request.method == 'POST':
        reporte.delete()
        messages.success(request, 'Reporte eliminado correctamente.')
        return redirect('lista_reportes')
    return render(request, 'reportes/eliminar_confirmar.html', {'reporte': reporte})

@login_required
def cambiar_estado(request, pk):
    # Buscamos el reporte (aquí podrías quitar el usuario=request.user si quieres que
    # cualquier admin pueda cambiar el de todos, pero por ahora dejémoslo así)
    reporte = get_object_or_404(Reporte, pk=pk)
    
    if reporte.estado == 'PENDIENTE':
        reporte.estado = 'PROCESO'
    elif reporte.estado == 'PROCESO':
        reporte.estado = 'RESUELTO'
    else:
        reporte.estado = 'PENDIENTE' # Por si quieres resetearlo
        
    reporte.save()
    messages.info(request, f'Estado de "{reporte.titulo}" actualizado a {reporte.estado}.')
    return redirect('lista_reportes')
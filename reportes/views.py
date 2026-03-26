from django.shortcuts import render, redirect, get_object_or_404
from .models import Reporte
from .forms import ReporteForm


def lista_reportes(request):
    reportes = Reporte.objects.all().order_by('estado', '-fecha_creacion')
    return render(request, 'reportes/lista_reportes.html', {'reportes': reportes})


def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes')
    else:
        form = ReporteForm()

    return render(request, 'reportes/crear_reporte.html', {'form': form})


def editar_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)

    if request.method == 'POST':
        form = ReporteForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes')
    else:
        form = ReporteForm(instance=reporte)

    return render(request, 'reportes/editar_reporte.html', {'form': form})


def eliminar_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    reporte.delete()
    return redirect('lista_reportes')


def cambiar_estado(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)

    if reporte.estado == "PENDIENTE":
        reporte.estado = "EN_PROCESO"
    elif reporte.estado == "EN_PROCESO":
        reporte.estado = "RESUELTO"
        reporte.prioridad = "NONE"

    reporte.save()
    return redirect('lista_reportes')
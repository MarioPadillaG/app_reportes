from django.contrib import admin
from .models import Categoria, Reporte

# Esto hace que aparezcan en el panel que ves en tu captura
admin.site.register(Categoria)
admin.site.register(Reporte)
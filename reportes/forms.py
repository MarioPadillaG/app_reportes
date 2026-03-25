from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['titulo', 'descripcion', 'lugar_especifico', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Falla proyector'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lugar_especifico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Edificio K, Aula 4'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }
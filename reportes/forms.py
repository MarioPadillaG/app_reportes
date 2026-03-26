from django import forms
from .models import Reporte, Categoria

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = [
            'titulo',
            'descripcion',
            'lugar_especifico',
            'categoria',
            'prioridad'
        ]

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'lugar_especifico': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 FIX DEL PROBLEMA ORIGINAL
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].empty_label = "Selecciona una categoría"

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError("Debes seleccionar una categoría.")
        return categoria
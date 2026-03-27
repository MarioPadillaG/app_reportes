from django import forms
from .models import Reporte, Categoria
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class RegistroForm(UserCreationForm):
    # Campo de email obligatorio y con validación
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Solo mostramos el email en el formulario
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Validación manual de @ y formato
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Introduce una dirección de correo válida (debe incluir '@').")
        
        # Verificar que no exista ya ese "username" (que es el email)
        if User.objects.filter(username=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # TRUCO: El username de Django será el correo
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['titulo', 'descripcion', 'lugar_especifico', 'categoria', 'prioridad']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lugar_especifico': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].empty_label = "Selecciona una categoría"

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo
import re
from django import forms
from .models import Reporte, Categoria
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# --- FORMULARIO DE REGISTRO (SOLO EMAIL) ---
class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",) 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Introduce una dirección de correo válida.")

        if User.objects.filter(username=email).exists():
            raise ValidationError("Este correo ya está registrado en el sistema.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# --- FORMULARIO DE REPORTES (BLINDADO CONTRA TROLEOS) ---
class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['titulo', 'descripcion', 'lugar_especifico', 'categoria', 'prioridad']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Proyector fundido'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe la falla con palabras reales...'}),
            'lugar_especifico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Edificio K, Aula 4'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].empty_label = "Selecciona una categoría"

    # --- VALIDACIONES DE SEGURIDAD AVANZADA ---

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo').strip()
        
        # 1. Obliga a que tenga al menos una LETRA (bloquea puros números como 33333)
        if not re.search(r'[a-zA-Z]', titulo):
            raise ValidationError("El título debe contener letras descriptivas.")

        # 2. Bloquea caracteres repetidos más de 3 veces (bloquea 3333 o aaaa)
        if re.search(r'(.)\1{3,}', titulo):
            raise ValidationError("No uses caracteres repetidos innecesarios.")

        if len(titulo) < 5:
            raise ValidationError("El título es demasiado corto.")
        return titulo

    def clean_descripcion(self):
        desc = self.cleaned_data.get('descripcion').strip()
        
        # 1. Bloquea el "Keyboard Smash" (texto largo sin espacios como el de tu imagen)
        # Si hay más de 15 letras seguidas sin un espacio, es basura.
        if re.search(r'[a-zA-Z0-9]{15,}', desc) and " " not in desc:
            raise ValidationError("La descripción parece texto al azar. Usa espacios y palabras reales.")

        # 2. Bloquea caracteres repetidos exagerados
        if re.search(r'(.)\1{4,}', desc):
            raise ValidationError("No rellenes la descripción con el mismo carácter.")

        if len(desc) < 10:
            raise ValidationError("Por favor, explica la falla con al menos 10 caracteres.")
        return desc

    def clean_lugar_especifico(self):
        lugar = self.cleaned_data.get('lugar_especifico').strip()
        
        # 1. Obliga a usar letras (bloquea puros números o símbolos)
        if not re.search(r'[a-zA-Z]', lugar):
            raise ValidationError("Indica una ubicación válida con letras (ej: Aula 4).")

        # 2. Bloquea símbolos repetidos (bloquea ¿¿¿¿ o ----)
        if re.search(r'[^a-zA-Z0-9\s]', lugar) and not re.search(r'[a-zA-Z0-9]', lugar):
             raise ValidationError("La ubicación no puede ser solo símbolos.")

        if len(lugar) < 3:
            raise ValidationError("La ubicación es muy corta.")
        return lugar

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise ValidationError("Debes elegir una categoría válida.")
        return categoria
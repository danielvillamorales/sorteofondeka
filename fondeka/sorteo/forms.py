from django.forms import ModelForm, EmailInput,TextInput
from .models import Empleados, Premios

class EmpleadosForm(ModelForm):
    class Meta:
        model = Empleados
        fields = ['cedula', 'nombre']
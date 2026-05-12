from django import forms
from .models import Usuario


class UsuarioPaso1Form(forms.ModelForm):

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Usuario

        fields = [
            'nombre',
            'apellido',
            'ocupacion',
            'documento_identidad',
            'sexo',
            'edad',
            'fecha_nacimiento',
            'ciudad_nacimiento',
            'estado_nacimiento',
            'pais_nacimiento',
        ]


class UsuarioPaso2Form(forms.ModelForm):

    class Meta:
        model = Usuario

        fields = [
            'direccion',
            'colonia_barrio',
            'codigo_postal',
            'telefono_movil',
            'correo_electronico',
        ]
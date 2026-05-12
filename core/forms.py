from django import forms
from .models import Usuario
import os


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

class UsuarioPaso3Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'grupo_sanguineo',
            'alergias',
            'tiene_padecimiento_fisico',
            'descripcion_padecimiento_fisico',
            'bajo_tratamiento_medico',
            'descripcion_tratamiento_medico',
            'toma_medicamentos',
            'descripcion_medicamentos',
            'tiene_seguro_medico',
            'descripcion_seguro_medico',
        ]
        widgets = {
            'descripcion_padecimiento_fisico': forms.Textarea(attrs={'rows': 3}),
            'descripcion_tratamiento_medico':  forms.Textarea(attrs={'rows': 3}),
            'descripcion_medicamentos':        forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'tiene_padecimiento_fisico': '¿Sufre de algún padecimiento físico?',
            'bajo_tratamiento_medico':   '¿Está bajo algún tratamiento médico?',
            'toma_medicamentos':         '¿Toma algún medicamento?',
            'tiene_seguro_medico':       '¿Posee seguro médico?',
            'descripcion_padecimiento_fisico': 'Especifique el padecimiento',
            'descripcion_tratamiento_medico':  'Especifique el tratamiento',
            'descripcion_medicamentos':        'Especifique medicamentos y forma de suministro',
            'descripcion_seguro_medico':       'Especifique el seguro médico',
        }

    def clean(self):
        cleaned_data = super().clean()

        # Si marcó "sí" pero dejó la descripción vacía → error
        pares = [
            ('tiene_padecimiento_fisico', 'descripcion_padecimiento_fisico',
             'Por favor especifique el padecimiento físico.'),
            ('bajo_tratamiento_medico', 'descripcion_tratamiento_medico',
             'Por favor especifique el tratamiento médico.'),
            ('toma_medicamentos', 'descripcion_medicamentos',
             'Por favor especifique medicamentos y forma de suministro.'),
            ('tiene_seguro_medico', 'descripcion_seguro_medico',
             'Por favor especifique el seguro médico.'),
        ]
        for bool_field, desc_field, msg in pares:
            if cleaned_data.get(bool_field) and not (cleaned_data.get(desc_field) or '').strip():
                self.add_error(desc_field, msg)

        return cleaned_data
    
class UsuarioPaso4Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'contacto_nombre',
            'contacto_apellido',
            'contacto_parentesco',
            'contacto_direccion',
            'contacto_colonia_barrio',
            'contacto_codigo_postal',
            'contacto_telefono_movil',
            'contacto2_nombre',
            'contacto2_apellido',
            'contacto2_telefono_movil',
        ]
        labels = {
            'contacto_nombre':           'Nombre del contacto de emergencia',
            'contacto_apellido':         'Apellido',
            'contacto_parentesco':       'Parentesco',
            'contacto_direccion':        'Dirección',
            'contacto_colonia_barrio':   'Colonia / Barrio',
            'contacto_codigo_postal':    'Código postal',
            'contacto_telefono_movil':   'Teléfono móvil',
            'contacto2_nombre':          'Nombre del contacto alternativo (opcional)',
            'contacto2_apellido':        'Apellido',
            'contacto2_telefono_movil':  'Teléfono móvil',
        }

    def clean(self):
        cleaned_data = super().clean()

        c2_fields = ['contacto2_nombre', 'contacto2_apellido', 'contacto2_telefono_movil']
        c2_values = [(cleaned_data.get(f) or '').strip() for f in c2_fields]

        if any(c2_values) and not all(c2_values):
            for field, value in zip(c2_fields, c2_values):
                if not value:
                    self.add_error(field, 'Si registra un contacto alternativo, complete los tres campos.')

        return cleaned_data

class UsuarioPaso5Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['modelo_vehiculo', 'placa_vehiculo']
        labels = {
            'modelo_vehiculo': 'Modelo del vehículo',
            'placa_vehiculo':  'Placa del vehículo',
        }


EXTENSIONES_PERMITIDAS = ['.pdf', '.jpg', '.jpeg', '.png']
TAMANO_MAXIMO_MB = 5


def _validar_archivo(archivo, etiqueta_campo):
    """Valida extensión y tamaño. Devuelve lista de errores."""
    errores = []
    if not archivo:
        return errores

    nombre = archivo.name.lower()
    extension = os.path.splitext(nombre)[1]
    if extension not in EXTENSIONES_PERMITIDAS:
        errores.append(
            f'{etiqueta_campo}: formato no permitido. '
            f'Use {", ".join(EXTENSIONES_PERMITIDAS)}.'
        )

    if archivo.size > TAMANO_MAXIMO_MB * 1024 * 1024:
        errores.append(
            f'{etiqueta_campo}: el archivo excede {TAMANO_MAXIMO_MB} MB.'
        )

    return errores


class UsuarioPaso6Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['documento_vehiculo', 'documento_identificacion']
        labels = {
            'documento_vehiculo':       'Documento del vehículo (PDF/JPG/PNG)',
            'documento_identificacion': 'Identificación oficial (PDF/JPG/PNG)',
        }
        widgets = {
            'documento_vehiculo':       forms.ClearableFileInput(
                attrs={'accept': '.pdf,.jpg,.jpeg,.png'}
            ),
            'documento_identificacion': forms.ClearableFileInput(
                attrs={'accept': '.pdf,.jpg,.jpeg,.png'}
            ),
        }

    def clean_documento_vehiculo(self):
        archivo = self.cleaned_data.get('documento_vehiculo')
        for err in _validar_archivo(archivo, 'Documento del vehículo'):
            raise forms.ValidationError(err)
        return archivo

    def clean_documento_identificacion(self):
        archivo = self.cleaned_data.get('documento_identificacion')
        for err in _validar_archivo(archivo, 'Identificación'):
            raise forms.ValidationError(err)
        return archivo

class UsuarioPaso7Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'acepta_liberacion_responsabilidad',
            'acepta_tratamiento_datos',
            'acepta_permiso_fotografias',
            'firma_conformidad',
        ]
        labels = {
            'acepta_liberacion_responsabilidad': 'Acepto la Liberación de Responsabilidad Social.',
            'acepta_tratamiento_datos':          'Acepto la Política de Privacidad.',
            'acepta_permiso_fotografias':        'Acepto el Permiso de Fotografías.',
            'firma_conformidad':                 'Firma de conformidad (PDF/JPG/PNG)',
        }
        widgets = {
            'firma_conformidad': forms.ClearableFileInput(
                attrs={'accept': '.pdf,.jpg,.jpeg,.png'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        obligatorios = [
            ('acepta_liberacion_responsabilidad',
             'Debe aceptar la Liberación de Responsabilidad Social para finalizar.'),
            ('acepta_tratamiento_datos',
             'Debe aceptar la Política de Privacidad para finalizar.'),
            ('acepta_permiso_fotografias',
             'Debe aceptar el Permiso de Fotografías para finalizar.'),
        ]
        for field, msg in obligatorios:
            if not cleaned_data.get(field):
                self.add_error(field, msg)

        if not cleaned_data.get('firma_conformidad'):
            self.add_error('firma_conformidad', 'Debe adjuntar la firma de conformidad.')

        return cleaned_data

    def clean_firma_conformidad(self):
        archivo = self.cleaned_data.get('firma_conformidad')
        for err in _validar_archivo(archivo, 'Firma de conformidad'):
            raise forms.ValidationError(err)
        return archivo
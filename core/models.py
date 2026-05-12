from django.db import models


class Usuario(models.Model):

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    PAISES_CHOICES = [
        ('Mexico', 'México'),
        ('Argentina', 'Argentina'),
        ('Colombia', 'Colombia'),
        ('Chile', 'Chile'),
        ('Peru', 'Perú'),
        ('España', 'España'),
        ('USA', 'Estados Unidos'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    ocupacion = models.CharField(max_length=100)

    documento_identidad = models.CharField(
        max_length=30,
        unique=True
    )

    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES
    )

    edad = models.IntegerField()

    fecha_nacimiento = models.DateField()

    ciudad_nacimiento = models.CharField(max_length=100)

    estado_nacimiento = models.CharField(max_length=100)

    pais_nacimiento = models.CharField(
        max_length=50,
        choices=PAISES_CHOICES
    )

    direccion = models.CharField(max_length=255)

    colonia_barrio = models.CharField(max_length=100)

    codigo_postal = models.CharField(max_length=20)

    telefono_movil = models.CharField(max_length=20)

    correo_electronico = models.EmailField(unique=True)

    GRUPO_SANGUINEO_CHOICES = [
    ('O+', 'O+'), ('O-', 'O-'),
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    # --- Información médica ---
    grupo_sanguineo = models.CharField(
        max_length=3,
        choices=GRUPO_SANGUINEO_CHOICES,
    )
    alergias = models.CharField(
        max_length=255,
        blank=True,
        help_text='Si no tiene alergias, escriba "Ninguna".'
    )

    tiene_padecimiento_fisico = models.BooleanField(default=False)
    descripcion_padecimiento_fisico = models.TextField(blank=True)

    bajo_tratamiento_medico = models.BooleanField(default=False)
    descripcion_tratamiento_medico = models.TextField(blank=True)

    toma_medicamentos = models.BooleanField(default=False)
    descripcion_medicamentos = models.TextField(
        blank=True,
        help_text='Incluya nombre del medicamento y forma de suministro.'
    )

    tiene_seguro_medico = models.BooleanField(default=False)
    descripcion_seguro_medico = models.CharField(max_length=255, blank=True)

    # --- Contacto de emergencia (principal) ---
    PARENTESCO_CHOICES = [
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Hermano/a', 'Hermano/a'),
        ('Esposo/a', 'Esposo/a'),
        ('Hijo/a', 'Hijo/a'),
        ('Pareja', 'Pareja'),
        ('Amigo/a', 'Amigo/a'),
        ('Otro', 'Otro'),
    ]

    contacto_nombre = models.CharField(max_length=100)
    contacto_apellido = models.CharField(max_length=100)
    contacto_parentesco = models.CharField(
        max_length=20,
        choices=PARENTESCO_CHOICES,
    )
    contacto_direccion = models.CharField(max_length=255)
    contacto_colonia_barrio = models.CharField(max_length=100)
    contacto_codigo_postal = models.CharField(max_length=20)
    contacto_telefono_movil = models.CharField(max_length=20)

    # --- Contacto alternativo (opcional) ---
    contacto2_nombre = models.CharField(max_length=100, blank=True)
    contacto2_apellido = models.CharField(max_length=100, blank=True)
    contacto2_telefono_movil = models.CharField(max_length=20, blank=True)

    # --- Vehículo ---
    modelo_vehiculo = models.CharField(max_length=100)
    placa_vehiculo = models.CharField(max_length=20, unique=True)

    # --- Documentos ---
    documento_vehiculo = models.FileField(upload_to='documentos_vehiculo/')
    documento_identificacion = models.FileField(upload_to='identificaciones/')

    # --- Aspectos legales (paso 7) ---
    acepta_liberacion_responsabilidad = models.BooleanField(default=False)
    acepta_tratamiento_datos = models.BooleanField(default=False)
    acepta_permiso_fotografias = models.BooleanField(default=False)
    fecha_aceptacion_legal = models.DateTimeField(null=True, blank=True)
    firma_conformidad = models.FileField(upload_to='firmas/', null=True, blank=True)

    # Bandera para saber si el registro terminó el paso 7
    registro_completo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
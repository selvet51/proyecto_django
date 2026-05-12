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

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
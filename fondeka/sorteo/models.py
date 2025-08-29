from django.db import models

# Create your models here.


class Empleados(models.Model):
    cedula = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=250)
    estado = models.CharField(
        max_length=1, default="A", help_text="A=Activo, I=Inactivo"
    )

    def __str__(self):
        return f"{self.cedula} {self.nombre}"


class Premios(models.Model):
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    fecha_sorteo = models.DateField()

    def __str__(self):
        return f"{self.empleado} {self.fecha_sorteo}"


class PremiosCopia(models.Model):
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    fecha_sorteo = models.DateField()

    def __str__(self):
        return f"{self.empleado} {self.fecha_sorteo}"

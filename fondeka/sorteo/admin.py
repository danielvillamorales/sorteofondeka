from django.contrib import admin
from .models import Empleados, Premios

# Register your models here.


class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombre", "estado")
    search_fields = ("cedula", "nombre")
    list_filter = ("estado",)


admin.site.register(Empleados, EmpleadosAdmin)


class PremiosAdmin(admin.ModelAdmin):
    list_display = ("empleado__cedula", "empleado__nombre", "fecha_sorteo")
    search_fields = ("empleado__nombre", "empleado__cedula")
    list_filter = ("fecha_sorteo",)


admin.site.register(Premios, PremiosAdmin)

from django.shortcuts import render
from .models import Empleados, Premios
from .forms import EmpleadosForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import datetime

# Create your views here.


@login_required
def listar_empleados(request):
    # Obtener el término de búsqueda
    search_query = request.GET.get("search", "")

    # Filtrar empleados según la búsqueda
    if search_query:
        empleados = Empleados.objects.filter(
            Q(nombre__icontains=search_query) | Q(cedula__icontains=search_query)
        ).order_by("nombre")
    else:
        empleados = Empleados.objects.all().order_by("nombre")

    # Paginación
    paginator = Paginator(empleados, 10)  # 10 empleados por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "empleados": page_obj,
        "search_query": search_query,
        "total_empleados": empleados.count(),
        "empleados_activos": empleados.filter(estado="A").count(),
        "empleados_inactivos": empleados.filter(estado="I").count(),
    }

    return render(request, "listar_empleados.html", context)


@login_required
def agregar_empleado(request):
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            cedula = request.POST.get("cedula")
            nombre = request.POST.get("nombre")
            estado = request.POST.get("estado", "A")  # Por defecto activo

            # Validaciones básicas
            if not cedula or not nombre:
                messages.error(request, "Todos los campos son obligatorios")
                return render(request, "agregar_empleado.html")

            if len(cedula) < 8:
                messages.error(request, "La cédula debe tener al menos 8 dígitos")
                return render(request, "agregar_empleado.html")

            # Verificar si la cédula ya existe
            if Empleados.objects.filter(cedula=cedula).exists():
                messages.error(request, "Ya existe un empleado con esa cédula")
                return render(request, "agregar_empleado.html")

            # Crear el empleado
            empleado = Empleados.objects.create(
                cedula=cedula, nombre=nombre, estado=estado
            )

            messages.success(request, f"Empleado {nombre} agregado correctamente")
            return redirect("listar_empleados")

        except Exception as e:
            messages.error(request, f"Error al agregar empleado: {str(e)}")
            return render(request, "agregar_empleado.html")

    return render(request, "agregar_empleado.html")


@login_required
def activar(request, pk):
    empleado = get_object_or_404(Empleados, pk=pk)
    empleado.estado = "A"
    empleado.save()
    messages.success(request, "Empleado activado correctamente")
    return redirect("listar_empleados")


@login_required
def inactivar(request, pk):
    empleado = get_object_or_404(Empleados, pk=pk)
    empleado.estado = "I"
    empleado.save()
    messages.success(request, "Empleado inactivado correctamente")
    return redirect("listar_empleados")


@login_required
def empleados_ganadores(request):
    # Obtener parámetros de filtro
    search_query = request.GET.get("search", "")
    fecha_filter = request.GET.get("fecha", "")

    # Filtrar empleados ganadores
    empleados = Premios.objects.all()

    # Filtro por búsqueda (nombre o cédula)
    if search_query:
        empleados = empleados.filter(
            Q(empleado__nombre__icontains=search_query)
            | Q(empleado__cedula__icontains=search_query)
        )

    # Filtro por fecha
    if fecha_filter:
        empleados = empleados.filter(fecha_sorteo=fecha_filter)

    # Ordenar por fecha más reciente
    empleados = empleados.order_by("-fecha_sorteo")

    # Obtener fechas únicas para el filtro
    fechas_disponibles = (
        Premios.objects.values_list("fecha_sorteo", flat=True)
        .distinct()
        .order_by("-fecha_sorteo")
    )

    # Crear lista de fechas con formato para el template
    fechas_formateadas = []
    for fecha in fechas_disponibles:
        fechas_formateadas.append(
            {
                "fecha": fecha,
                "formato_ymd": fecha.strftime("%Y-%m-%d"),
                "formato_display": fecha.strftime("%d/%m/%Y"),
                "selected": (
                    fecha_filter == fecha.strftime("%Y-%m-%d")
                    if fecha_filter
                    else False
                ),
            }
        )

    # Paginación
    paginator = Paginator(empleados, 10)  # 10 ganadores por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "empleados": page_obj,
        "search_query": search_query,
        "fecha_filter": fecha_filter,
        "fechas_disponibles": fechas_disponibles,
        "fechas_formateadas": fechas_formateadas,
        "total_ganadores": empleados.count(),
        "fechas_unicas": len(fechas_disponibles),
    }

    return render(request, "empleados_ganadores.html", context)


@login_required
def sorteo(request):
    empleados_aleatorios = Premios.objects.none()
    empleados_seleccionados = list(empleados_aleatorios)
    if request.method == "POST":
        numero = request.POST.get("numero")
        empleados = Empleados.objects.filter(estado="A").exclude(premios__isnull=False)
        cristian = Empleados.objects.get(cedula="1112779920")
        numero = len(empleados) if int(numero) > len(empleados) else numero
        c_estado = Premios.objects.filter(empleado=cristian).count()
        if cristian.estado == "A" and c_estado == 0:
            print("entro a restar")
            numero = int(numero) - 1

        empleados_aleatorios = empleados.order_by("?")[: int(numero)]

        # Crear un objeto Premios para cada empleado seleccionado
        try:
            for empleado in empleados_aleatorios:
                premio = Premios(empleado=empleado, fecha_sorteo=datetime.date.today())
                premio.save()
            messages.success(request, "Sorteo realizado correctamente")
        except Exception as e:
            messages.error(request, "Error al realizar sorteo" + str(e))

        empleados_seleccionados = list(empleados_aleatorios)
        if cristian.estado == "A" and c_estado == 0:
            empleados_seleccionados.append(cristian)
            empleado = Premios(empleado=cristian, fecha_sorteo=datetime.date.today())
            empleado.save()

    return render(request, "sorteo.html", {"empleados": empleados_seleccionados})


@login_required
def reiniciar(request):
    premios = Premios.objects.all().delete()
    messages.success(request, "Reinicio realizado correctamente")
    return redirect("empleados_ganadores")

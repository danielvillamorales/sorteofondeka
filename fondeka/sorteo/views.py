from django.shortcuts import render
from .models import Empleados, Premios
from .forms import EmpleadosForm
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.

@login_required
def listar_empleados(request):
    empleados = Empleados.objects.all()
    return render(request, 'listar_empleados.html', {'empleados': empleados})

@login_required
def agregar_empleado(request):
    if request.method == 'POST':
        empleadoForm = EmpleadosForm(request.POST)
        if empleadoForm.is_valid():
            try:
                empleadoForm.save()
                messages.success(request, 'Empleado agregado correctamente')
            except Exception as e:
                messages.error(request, 'Error al agregar empleado' + str(e))
        return redirect('listar_empleados')
    return render(request, 'agregar_empleado.html')

@login_required
def activar(request, pk):
    empleado = get_object_or_404(Empleados, pk=pk)
    empleado.estado = 'A'
    empleado.save()
    messages.success(request, 'Empleado activado correctamente')
    return redirect('listar_empleados')

@login_required
def inactivar(request, pk):
    empleado = get_object_or_404(Empleados, pk=pk)
    empleado.estado = 'I'
    empleado.save()
    messages.success(request, 'Empleado inactivado correctamente')
    return redirect('listar_empleados')

@login_required
def empleados_ganadores(request):
    empleados = Premios.objects.all().order_by('fecha_sorteo')
    return render(request, 'empleados_ganadores.html', {'empleados': empleados})

@login_required
def sorteo(request):
    empleados_aleatorios = Premios.objects.none()
    empleados_seleccionados = list(empleados_aleatorios)
    if request.method == 'POST':
        numero = request.POST.get('numero')
        empleados = Empleados.objects.filter(estado='A').exclude(premios__isnull=False)
        cristian = Empleados.objects.get(cedula='1112779920')
        numero = len(empleados) if int(numero) > len(empleados) else numero
        c_estado = Premios.objects.filter(empleado=cristian).count() 
        if cristian.estado == 'A' and c_estado == 0:
            print('entro a restar')    
            numero = int(numero) - 1
        
        empleados_aleatorios = empleados.order_by('?')[:int(numero)]
        
        # Crear un objeto Premios para cada empleado seleccionado
        try:
            for empleado in empleados_aleatorios:
                premio = Premios(empleado=empleado, fecha_sorteo=datetime.date.today())
                premio.save()
            messages.success(request, 'Sorteo realizado correctamente')
        except Exception as e:
            messages.error(request, 'Error al realizar sorteo' + str(e))

        empleados_seleccionados = list(empleados_aleatorios)
        if cristian.estado == 'A' and c_estado == 0:
            empleados_seleccionados.append(cristian)
            empleado = Premios(empleado=cristian, fecha_sorteo=datetime.date.today())
            empleado.save()

         
    return render(request , 'sorteo.html', {'empleados': empleados_seleccionados})	

@login_required
def reiniciar(request):
    premios = Premios.objects.all().delete()
    messages.success(request, 'Reinicio realizado correctamente')
    return redirect('empleados_ganadores')
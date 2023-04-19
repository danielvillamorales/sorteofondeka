"""fondeka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sorteo.views import listar_empleados, agregar_empleado, activar, inactivar, empleados_ganadores, sorteo, reiniciar
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('accounts/login/',LoginView.as_view(template_name='login.html'),name="login"),
    path('',LoginView.as_view(template_name='login.html'),name="login"),
    path('accounts/logout/',LogoutView.as_view(template_name='logout.html'),name="logout"),
    path('admin/', admin.site.urls),
    path('listar_empleados/', listar_empleados, name='listar_empleados'),
    path('agregar_empleado/', agregar_empleado, name='agregar_empleado'),
    path('activar/<int:pk>', activar, name='activar'),
    path('inactivar/<int:pk>', inactivar, name='inactivar'),
    path('empleados_ganadores/', empleados_ganadores, name='empleados_ganadores'),
    path('sorteo/', sorteo, name='sorteo'),
    path('reiniciar/', reiniciar, name='reiniciar'),
]

# Generated by Django 4.1.7 on 2023-04-19 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=250)),
                ('estado', models.CharField(default='A', help_text='A=Activo, I=Inactivo', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Premios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_sorteo', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sorteo.empleados')),
            ],
        ),
    ]

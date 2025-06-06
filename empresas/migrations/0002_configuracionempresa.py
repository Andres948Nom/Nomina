# Generated by Django 5.1.7 on 2025-06-01 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignacion_basica_anual', models.DecimalField(decimal_places=2, default=1300000, max_digits=12)),
                ('auxilio_transporte', models.DecimalField(decimal_places=2, default=162000, max_digits=12)),
                ('intensidad_horaria', models.PositiveIntegerField(default=48)),
                ('porcentaje_salud', models.DecimalField(decimal_places=2, default=4.0, max_digits=5)),
                ('porcentaje_pension', models.DecimalField(decimal_places=2, default=4.0, max_digits=5)),
                ('porcentaje_riesgos', models.DecimalField(decimal_places=2, default=0.52, max_digits=5)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configuracion', to='empresas.empresa')),
            ],
        ),
    ]

# Generated by Django 5.1.7 on 2025-06-03 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0003_alter_configuracionempresa_asignacion_basica_anual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracionempresa',
            name='intensidad_horaria',
            field=models.PositiveIntegerField(default=230),
        ),
    ]

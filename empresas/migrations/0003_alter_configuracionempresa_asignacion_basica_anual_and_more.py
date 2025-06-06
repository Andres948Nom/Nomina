# Generated by Django 5.1.7 on 2025-06-02 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0002_configuracionempresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracionempresa',
            name='asignacion_basica_anual',
            field=models.DecimalField(decimal_places=2, default=1423500, max_digits=12),
        ),
        migrations.AlterField(
            model_name='configuracionempresa',
            name='auxilio_transporte',
            field=models.DecimalField(decimal_places=2, default=200000, max_digits=12),
        ),
    ]

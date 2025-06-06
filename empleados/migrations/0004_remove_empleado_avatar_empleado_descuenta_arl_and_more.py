# Generated by Django 5.1.7 on 2025-06-02 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0003_cargo_gruponomina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='avatar',
        ),
        migrations.AddField(
            model_name='empleado',
            name='descuenta_arl',
            field=models.BooleanField(default=True, help_text='Indica si al empleado se le descuenta el aporte a riesgos laborales.'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='descuenta_pension',
            field=models.BooleanField(default=True, help_text='Indica si al empleado se le descuenta el aporte a pensión.'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='descuenta_salud',
            field=models.BooleanField(default=True, help_text='Indica si al empleado se le descuenta el aporte a salud.'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='actualizado_en',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

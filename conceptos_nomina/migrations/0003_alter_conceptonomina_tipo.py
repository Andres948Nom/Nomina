# Generated by Django 5.1.7 on 2025-06-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conceptos_nomina', '0002_alter_conceptonomina_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conceptonomina',
            name='tipo',
            field=models.CharField(choices=[('DEVENGADO', 'Devengado'), ('DEDUCCION', 'Deducción'), ('PROVISION', 'Provisión'), ('INFORMATIVO', 'Informativo'), ('PARAFISCALES', 'Parafiscales')], help_text='Tipo de concepto', max_length=20),
        ),
    ]

# Generated by Django 4.2.17 on 2025-01-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetoapp', '0009_reserva_data_fim_reserva_data_inicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campo',
            name='preco_por_hora',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]

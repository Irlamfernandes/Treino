# Generated by Django 4.2.17 on 2025-01-07 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetoapp', '0008_remove_perfil_cidade_perfil_email_perfil_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='data_fim',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='data_inicio',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='campo',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='campo',
            name='preco_por_hora',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterUniqueTogether(
            name='campo',
            unique_together={('nome', 'cidade')},
        ),
        migrations.AlterUniqueTogether(
            name='perfil',
            unique_together={('email',)},
        ),
        migrations.AlterUniqueTogether(
            name='reserva',
            unique_together={('campo', 'data_inicio', 'data_fim')},
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='data_reserva',
        ),
    ]

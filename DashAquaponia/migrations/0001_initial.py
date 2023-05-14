# Generated by Django 4.1.9 on 2023-05-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtdeAlimentoPeixe', models.IntegerField(verbose_name='AlimentoPeixe')),
                ('limpezaAgua', models.BooleanField(verbose_name='LimpezaAgua')),
                ('peixeMorto', models.BooleanField(verbose_name='PeixeMorto')),
                ('capacidadeTanque', models.FloatField(verbose_name='CapacidadeTanque')),
                ('nomeCliente', models.CharField(max_length=75, verbose_name='Cliente')),
                ('statusTanque', models.CharField(max_length=75, verbose_name='Status')),
                ('valorAlface', models.FloatField(verbose_name='ValorAlface')),
                ('valorPeixe', models.FloatField(verbose_name='ValorPeixe')),
                ('dataInspecao', models.DateField(verbose_name='Data')),
                ('idCliente', models.IntegerField(verbose_name='IdCliente')),
                ('idTanque', models.IntegerField(verbose_name='IdTanque')),
                ('qtdeAgua', models.FloatField(verbose_name='qtdeAgua')),
                ('qtdeAlfaceColhida', models.IntegerField(verbose_name='AlfaceColhido')),
                ('qtdeAlfacePlantada', models.IntegerField(verbose_name='AlfacePlantado')),
                ('qtdePeixesTanque', models.IntegerField(verbose_name='PeixesNoTanque')),
            ],
            options={
                'db_table': 'AquaDash',
            },
        ),
    ]

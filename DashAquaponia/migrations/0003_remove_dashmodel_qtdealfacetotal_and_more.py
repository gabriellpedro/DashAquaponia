# Generated by Django 4.1.9 on 2024-05-19 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashAquaponia', '0002_dashmodel_qtdevendapeixe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashmodel',
            name='qtdeAlfaceTotal',
        ),
        migrations.AddField(
            model_name='dashmodel',
            name='qtdeVendaAlface',
            field=models.IntegerField(default=0, verbose_name='VendaAlface'),
            preserve_default=False,
        ),
    ]

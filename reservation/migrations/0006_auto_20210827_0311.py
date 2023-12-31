# Generated by Django 3.2.4 on 2021-08-27 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomservices', '0002_alter_service_name'),
        ('reservation', '0005_alter_perma_reservation_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='perma_reservation',
            name='service',
            field=models.ManyToManyField(to='roomservices.Service'),
        ),
        migrations.AddField(
            model_name='temp_reservation',
            name='service',
            field=models.ManyToManyField(to='roomservices.Service'),
        ),
    ]

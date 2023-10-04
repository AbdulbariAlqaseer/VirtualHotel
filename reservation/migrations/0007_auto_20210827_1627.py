# Generated by Django 3.2.4 on 2021-08-27 13:27

from django.db import migrations, models
import reservation.models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_auto_20210827_0311'),
    ]

    operations = [
        migrations.AddField(
            model_name='perma_reservation',
            name='guests',
            field=models.SmallIntegerField(default=1, validators=[reservation.models.is_pos]),
        ),
        migrations.AddField(
            model_name='temp_reservation',
            name='guests',
            field=models.SmallIntegerField(default=1, validators=[reservation.models.is_pos]),
        ),
    ]
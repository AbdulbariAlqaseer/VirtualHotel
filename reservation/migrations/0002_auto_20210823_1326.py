# Generated by Django 3.2.4 on 2021-08-23 10:26

from django.db import migrations, models
import reservation.models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perma_reservation',
            old_name='bill',
            new_name='bill_befor_discount',
        ),
        migrations.AddField(
            model_name='perma_reservation',
            name='bill_after_discount',
            field=models.IntegerField(default=0, validators=[reservation.models.is_pos]),
        ),
    ]

# Generated by Django 3.2.4 on 2021-08-23 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

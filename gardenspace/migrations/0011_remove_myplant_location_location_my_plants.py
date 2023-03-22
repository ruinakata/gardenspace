# Generated by Django 4.1.7 on 2023-03-15 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardenspace', '0010_location_myplant_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myplant',
            name='location',
        ),
        migrations.AddField(
            model_name='location',
            name='my_plants',
            field=models.ManyToManyField(to='gardenspace.myplant'),
        ),
    ]
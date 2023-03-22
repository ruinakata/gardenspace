# Generated by Django 4.1.7 on 2023-03-11 01:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gardenspace', '0005_myplant_state_myplant_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myplant',
            old_name='plant_id',
            new_name='plant',
        ),
        migrations.RemoveField(
            model_name='myplant',
            name='user_id',
        ),
        migrations.AddField(
            model_name='myplant',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

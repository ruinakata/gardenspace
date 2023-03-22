# Generated by Django 4.1.7 on 2023-03-07 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(max_length=50)),
                ('scientific_name', models.CharField(blank=True, default='', max_length=50)),
                ('germination_temperature', models.IntegerField(blank=True)),
                ('requires_stratification', models.BooleanField(blank=True, default=False)),
                ('optimum_low_temp', models.IntegerField(blank=True)),
                ('optimum_high_temp', models.IntegerField(blank=True)),
            ],
            options={
                'ordering': ['common_name'],
            },
        ),
    ]

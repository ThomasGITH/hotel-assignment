# Generated by Django 5.1.3 on 2024-11-24 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hotelapp.city')),
            ],
        ),
    ]

# Generated by Django 4.0.3 on 2022-03-10 16:18

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0006_alter_section_time_slot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='year',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1701, 1, 1)), django.core.validators.MaxValueValidator(datetime.date(2100, 1, 1))]),
        ),
    ]

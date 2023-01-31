# Generated by Django 4.1.5 on 2023-01-31 20:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='date_mailing',
            field=models.DateTimeField(null=True, verbose_name='Дата удачной рассылки'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 31, 23, 54, 4, 110375), verbose_name='Дата и время последней попытки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='time_mailing_end',
            field=models.TimeField(default=datetime.datetime(2023, 1, 31, 23, 54, 4, 109374), null=True, verbose_name='Время окончания рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='time_mailing_start',
            field=models.TimeField(default=datetime.datetime(2023, 1, 31, 23, 54, 4, 109374), null=True, verbose_name='Время начала рассылки'),
        ),
    ]

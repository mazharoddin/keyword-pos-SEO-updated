# Generated by Django 2.2 on 2020-11-18 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyservice', '0007_mapposition'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapposition',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='position',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]

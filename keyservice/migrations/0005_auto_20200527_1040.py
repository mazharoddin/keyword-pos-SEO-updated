# Generated by Django 2.2 on 2020-05-27 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyservice', '0004_auto_20200522_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='priority_keyword',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='position',
            name='seq_no',
            field=models.IntegerField(default=0),
        ),
    ]

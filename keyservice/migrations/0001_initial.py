# Generated by Django 2.2 on 2020-04-11 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('urls', models.CharField(max_length=255)),
                ('main_keyword', models.TextField()),
                ('secondary_keyword', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('url', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
                ('keyword_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keyservice.Keyword')),
            ],
        ),
    ]
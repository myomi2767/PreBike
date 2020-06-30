# Generated by Django 3.0.7 on 2020-06-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rentGu', models.CharField(max_length=20)),
                ('rentDong', models.CharField(max_length=20)),
                ('stationName', models.CharField(max_length=100)),
                ('stationNum', models.IntegerField(default=0)),
                ('stationValue', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Recede',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recedeTime', models.CharField(max_length=20)),
                ('restationNum', models.IntegerField(default=0)),
                ('restationName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rentTime', models.CharField(max_length=20)),
                ('stationNum', models.IntegerField(default=0)),
                ('stationName', models.CharField(max_length=100)),
            ],
        ),
    ]

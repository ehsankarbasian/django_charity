# Generated by Django 3.1.7 on 2021-04-23 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0021_auto_20210423_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='list_of_needs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
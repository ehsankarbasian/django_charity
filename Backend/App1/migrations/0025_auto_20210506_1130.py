# Generated by Django 3.1.7 on 2021-05-06 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0024_auto_20210505_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='creator',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]

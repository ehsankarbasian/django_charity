# Generated by Django 3.1.7 on 2021-04-12 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0003_auto_20210412_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.BooleanField(choices=[(1, 'male'), (0, 'female')], default=1),
        ),
    ]

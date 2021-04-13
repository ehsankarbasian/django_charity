# Generated by Django 3.1.7 on 2021-04-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0002_userprofile_email_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.BooleanField(choices=[(1, 'male'), (0, 'female')], default=-1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Super admin'), (2, 'Admin'), (3, 'Donator'), (4, 'Needy')], default=-1),
        ),
    ]

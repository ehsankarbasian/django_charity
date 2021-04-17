# Generated by Django 3.1.7 on 2021-04-17 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0010_auto_20210417_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.BooleanField(choices=[(1, 'male'), (0, 'female')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='married',
            field=models.BooleanField(blank=True, choices=[(0, 'not married'), (1, 'married')], default=0, null=True),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-22 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0017_auto_20210423_0347'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='reset_pass_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

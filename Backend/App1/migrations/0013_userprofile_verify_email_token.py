# Generated by Django 3.1.7 on 2021-04-19 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0012_userprofile_reset_pass_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verify_email_token',
            field=models.CharField(default='', max_length=64),
        ),
    ]
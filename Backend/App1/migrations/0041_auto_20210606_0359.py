# Generated by Django 3.1.7 on 2021-06-05 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0040_userprofile_profile_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='create_date',
            field=models.DateField(auto_now=True),
        ),
    ]

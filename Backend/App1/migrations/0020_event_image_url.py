# Generated by Django 3.1.7 on 2021-04-23 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0019_event_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_url',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
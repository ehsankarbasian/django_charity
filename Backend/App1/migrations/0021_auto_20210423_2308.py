# Generated by Django 3.1.7 on 2021-04-23 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App1', '0020_event_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='edited_by',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0008_auto_20210417_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='job',
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
    ]
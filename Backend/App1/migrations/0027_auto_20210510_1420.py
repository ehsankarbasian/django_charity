# Generated by Django 3.1.7 on 2021-05-10 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0026_category_donatesin_donatesout_product_subcategory_transactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donatesin',
            name='donator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App1.userprofile'),
        ),
        migrations.AlterField(
            model_name='donatesout',
            name='delivered_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='admin', to='App1.userprofile'),
        ),
        migrations.AlterField(
            model_name='donatesout',
            name='delivered_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='needy', to='App1.userprofile'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='donatorOrNeedy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='App1.userprofile'),
        ),
    ]

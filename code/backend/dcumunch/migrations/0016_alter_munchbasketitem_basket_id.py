# Generated by Django 4.1.4 on 2023-02-21 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcumunch', '0015_munchbasketitem_munchbasket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='munchbasketitem',
            name='basket_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcumunch.munchbasket'),
        ),
    ]

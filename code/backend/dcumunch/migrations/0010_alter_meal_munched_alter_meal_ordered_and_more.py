# Generated by Django 4.1.4 on 2023-02-13 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcumunch', '0009_remove_meal_count_remove_recipe_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='munched',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='ordered',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='munched',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
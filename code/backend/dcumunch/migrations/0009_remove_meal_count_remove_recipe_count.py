# Generated by Django 4.1.4 on 2023-02-13 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dcumunch', '0008_meal_count_meal_munched_meal_ordered_recipe_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='count',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='count',
        ),
    ]

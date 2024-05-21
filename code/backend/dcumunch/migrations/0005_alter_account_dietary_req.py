# Generated by Django 4.1.4 on 2023-02-09 19:42

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dcumunch', '0004_alter_account_activity_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='dietary_req',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Cereals containing gluten'), (2, 'Crustaceans'), (3, 'Eggs'), (4, 'Fish'), (5, 'Peanuts'), (6, ' Soybeans'), (7, 'Milk (Lactose)'), (8, 'Nuts'), (9, 'Celery'), (10, 'Mustard'), (11, 'Sesame seeds'), (12, 'Sulphur dioxide and sulphites'), (13, 'Lupin'), (14, 'Molluscs'), (15, 'Pork'), (16, 'Beef')], max_length=100, null=True),
        ),
    ]
# Generated by Django 5.0.3 on 2024-04-30 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_inventory_description_inventory_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='playbook',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

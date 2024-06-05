# Generated by Django 5.0.3 on 2024-04-23 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_inventory_options_alter_status_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='inventory',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='playbook',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='playbook',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.group'),
        ),
        migrations.AlterField(
            model_name='playbook',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.group'),
        ),
    ]

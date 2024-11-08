# Generated by Django 5.0.3 on 2024-05-01 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_inventory_last_modified_playbook_last_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrunned',
            name='datetime',
        ),
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='job',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name_plural': 'Inventories'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'Status'},
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=14),
        ),
    ]

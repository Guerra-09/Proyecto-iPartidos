# Generated by Django 5.0 on 2023-12-16 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canchas', '0004_rename_maxplayers_field_playersperside_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='description',
            field=models.CharField(blank=True, choices=[('Pasto sintético', 'Pasto sintético'), ('Pasto real', 'Pasto real'), ('Cemento', 'Cemento'), ('Arcilla', 'Arcilla')], default='not defined', max_length=100, null=True),
        ),
    ]
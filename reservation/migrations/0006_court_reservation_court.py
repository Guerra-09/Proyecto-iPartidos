# Generated by Django 5.0 on 2023-12-18 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canchas', '0006_alter_field_description_alter_field_groundtype'),
        ('reservation', '0005_alter_reservation_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canchas.field')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='court',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reservation.court'),
        ),
    ]
# Generated by Django 4.2.7 on 2023-12-14 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_remove_reservation_field_rent_history'),
        ('registration', '0004_alter_client_options_alter_tenant_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldrenthistory',
            name='reservation',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='reservation.reservation'),
            preserve_default=False,
        ),
    ]

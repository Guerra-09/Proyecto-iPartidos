# Generated by Django 4.2.7 on 2023-12-06 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_rename_usuario_usuarioprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioprofile',
            name='email',
            field=models.EmailField(default='user@example.com', max_length=254),
        ),
    ]

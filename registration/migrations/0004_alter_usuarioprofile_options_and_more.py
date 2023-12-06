# Generated by Django 4.2.7 on 2023-12-06 04:06

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('registration', '0003_usuarioprofile_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuarioprofile',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='usuarioprofile',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='usuarioprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='usuario_profiles', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='password',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='usuario_profiles_permissions', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='usuarioprofile',
            name='username',
            field=models.CharField(default='', max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='usuarioprofile',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='usuarioprofile',
            name='last_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='usuarioprofile',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]

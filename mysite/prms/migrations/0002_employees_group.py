# Generated by Django 3.1.3 on 2020-11-26 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='group',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='User', max_length=5),
        ),
    ]

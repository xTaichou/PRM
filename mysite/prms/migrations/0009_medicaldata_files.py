# Generated by Django 3.1.3 on 2021-01-27 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0008_auto_20210127_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicaldata',
            name='files',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]

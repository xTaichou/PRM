# Generated by Django 3.1.3 on 2021-01-26 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0006_auto_20210126_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visits',
            name='files',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]

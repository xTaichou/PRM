# Generated by Django 3.1.3 on 2020-11-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0002_employees_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companybilling',
            name='amount',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
    ]

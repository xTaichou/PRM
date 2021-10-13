# Generated by Django 3.1.3 on 2021-01-18 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0004_auto_20201216_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='group',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Practitioner', 'Practitioner'), ('User', 'User')], default='User', max_length=12),
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Booking date&time')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prms.employees')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prms.patients')),
            ],
        ),
    ]

# Generated by Django 3.2 on 2022-11-21 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='service_type',
        ),
        migrations.AddField(
            model_name='booking',
            name='shipment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipment_type', to='core.standardcode'),
        ),
    ]

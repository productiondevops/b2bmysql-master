# Generated by Django 3.2 on 2023-04-27 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_barcodecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='declare_value',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='insurance_value',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]

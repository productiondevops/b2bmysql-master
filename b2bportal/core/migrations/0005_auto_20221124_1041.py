# Generated by Django 3.2 on 2022-11-24 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20221124_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='goods_description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerwaybill',
            name='goods_description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 3.2 on 2022-11-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_dimensions'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimensions',
            name='pieces',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]

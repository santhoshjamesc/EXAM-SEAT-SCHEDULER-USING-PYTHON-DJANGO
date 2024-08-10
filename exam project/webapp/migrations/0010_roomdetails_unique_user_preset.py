# Generated by Django 5.0.3 on 2024-07-15 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_admen'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='roomdetails',
            constraint=models.UniqueConstraint(fields=('user', 'preset_name'), name='unique_user_preset'),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-14 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_student_delete_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='phno',
            new_name='phone_number',
        ),
    ]

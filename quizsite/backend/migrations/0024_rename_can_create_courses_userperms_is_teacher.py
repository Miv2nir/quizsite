# Generated by Django 5.0.1 on 2024-05-30 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_userperms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userperms',
            old_name='can_create_courses',
            new_name='is_teacher',
        ),
    ]

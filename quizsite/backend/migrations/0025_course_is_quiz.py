# Generated by Django 5.0.1 on 2024-05-30 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_rename_can_create_courses_userperms_is_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_quiz',
            field=models.BooleanField(default=False),
        ),
    ]

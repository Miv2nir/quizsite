# Generated by Django 5.0.1 on 2024-06-12 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0042_alter_studentanswerfile_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='title',
            field=models.TextField(default=''),
        ),
    ]

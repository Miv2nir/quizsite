# Generated by Django 5.0.1 on 2024-05-24 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_coursepage_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursepage',
            name='has_answer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='coursepage',
            name='title',
            field=models.TextField(default=''),
        ),
    ]
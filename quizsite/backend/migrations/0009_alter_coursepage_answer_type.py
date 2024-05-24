# Generated by Django 5.0.1 on 2024-05-24 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_coursepage_answer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepage',
            name='answer_type',
            field=models.CharField(choices=[('T', 'Text'), ('C', 'Singular Choice'), ('M', 'Multiple Choice'), ('F', 'File Upload')], max_length=1),
        ),
    ]

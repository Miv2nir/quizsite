# Generated by Django 5.0.1 on 2024-05-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_remove_pageanswertext_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepage',
            name='answer_type',
            field=models.CharField(choices=[('N', None), ('T', 'Text'), ('s', 'Singular Choice'), ('M', 'Multiple Choice'), ('F', 'File Upload')], default='N', max_length=1),
        ),
    ]

# Generated by Django 5.0.1 on 2024-06-02 19:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0032_coursepage_time_pageanswertext_correct_grade_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAnswerFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_type', models.CharField(choices=[('N', None), ('T', 'Text'), ('S', 'Singular Choice'), ('M', 'Multiple Choice'), ('F', 'File Upload')], default='N', max_length=1)),
                ('response', models.FileField(default=None, upload_to='')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.coursepage')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

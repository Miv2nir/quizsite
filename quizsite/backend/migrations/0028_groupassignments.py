# Generated by Django 5.0.1 on 2024-05-30 22:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0027_userperms_is_manager_alter_groupenrollment_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAssignments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateTimeField(default=None, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.course')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.usergroups')),
            ],
        ),
    ]
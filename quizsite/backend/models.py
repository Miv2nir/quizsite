from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name=models.CharField(max_length=30)
    author=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ACCESS_LEVEL = (
        ('A','Public'),
        ('B','Unlisted'),
        ('C','Private'),
    )
    access=models.CharField(max_length=1,choices=ACCESS_LEVEL,default='C')

    def __str__(self):
        return self.name
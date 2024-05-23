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
    description=models.TextField(default='')
    access=models.CharField(max_length=1,choices=ACCESS_LEVEL,default='C')

    def __str__(self):
        return self.name

class CoursePage(models.Model):
    parent=models.ForeignKey(Course,on_delete=models.CASCADE)
    number=models.IntegerField()
    title=models.TextField(default=('Page '))
    text=models.TextField(default='')
    

    def __str__(self):
        return 'Page '+str(self.number)

    #setting a default title
    def save(self,*args,**kwargs):
        self.title=self.title+str(self.number)
        super().save(*args,**kwargs)
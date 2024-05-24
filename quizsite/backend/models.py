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
    title=models.TextField(default='')
    text=models.TextField(default='')
    has_answer=models.BooleanField(default=False)

    def __str__(self):
        return 'Page '+str(self.number)

#Answer form models
#Concept: several models each storing an answer for pages that have something to submit. Each submission is done by a specific user so that it can be pulled up later on.

class CoursePageAnswer(models.Model): #abstract parent
    page=models.OneToOneField(CoursePage,on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    class Meta:
        abstract=True
    def __str__(self):
        return 'Answer for '+str(self.page)+' by '+str(self.user)
class PageAnswerText(CoursePageAnswer):
    text=models.TextField(default='')
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
    #has_answer=models.BooleanField(default=False)

    ANSWER_TYPE = (
        ('N',None),
        ('T','Text'),
        ('S','Singular Choice'),
        ('M','Multiple Choice'),
        ('F','File Upload'),
    )
    answer_type=models.CharField(max_length=1,choices=ANSWER_TYPE,default='N')

    def __str__(self):
        return 'Page '+str(self.number)

#Answer form models
#Concept: several models each storing an answer for pages that have something to submit. Each submission is done by a specific user so that it can be pulled up later on.

class CoursePageAnswer(models.Model): #abstract parent
    page=models.OneToOneField(CoursePage,on_delete=models.CASCADE)
    #user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    class Meta:
        abstract=True
    def __str__(self):
        return 'Answer type for page '+str(self.page)

#testing out a different approach
class PageAnswerText(CoursePageAnswer):
    text=models.TextField(default='')
    is_choice=models.BooleanField(default=False)
    is_multiple=models.BooleanField(default=False)
    choices=models.JSONField(default=dict)


#this simply didn't work :(
'''
    def __init(self,*args,CHOICE_DATA=None,**kwargs):
        #CHOICE_DATA=kwargs.pop('CHOICE_DATA',None)
        super(PageAnswerText,self).__init__(*args,**kwargs)
        if CHOICE_DATA != None:
            self._apply_choices(CHOICE_DATA)
        
    def _apply_choices(self,CHOICE_DATA):
        if CHOICE_DATA:
            self.text=models.TextField(default='',choices=CHOICE_DATA)
        else:
            self.text=models.TextField(default='')

'''
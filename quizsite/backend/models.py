from django.db import models

from django.contrib.auth.models import User

from django.core.files.storage import FileSystemStorage

from django.conf import settings



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
    is_quiz=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.name=self.name.replace('/','').replace('?','')
        super(Course,self).save(*args,**kwargs)

class CoursePage(models.Model):
    parent=models.ForeignKey(Course,on_delete=models.CASCADE)
    number=models.IntegerField()
    title=models.TextField(default='')
    text=models.TextField(default='')
    is_quiz=models.BooleanField(default=False)
    #has_answer=models.BooleanField(default=False)

    ANSWER_TYPE = (
        ('N',None),
        ('T','Text'),
        ('S','Singular Choice'),
        ('M','Multiple Choice'),
        ('F','File Upload'),
    )
    answer_type=models.CharField(max_length=1,choices=ANSWER_TYPE,default='N')

    time=models.IntegerField(default=15,null=True)

    def __str__(self):
        return 'Page '+str(self.number)+' of '+self.parent.name

#Answer form models
#Concept: several models each storing an answer for pages that have something to submit. Each submission is done by a specific user so that it can be pulled up later on.

class CoursePageAnswer(models.Model): #abstract parent
    page=models.OneToOneField(CoursePage,on_delete=models.CASCADE)
    #user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    class Meta:
        abstract=True
    def __str__(self):
        return 'Answer type for page '+str(self.page.title)

#testing out a different approach
class PageAnswerText(CoursePageAnswer):
    text=models.TextField(default='',blank=True)
    is_choice=models.BooleanField(default=False)
    is_multiple=models.BooleanField(default=False)
    is_file=models.BooleanField(default=False)
    choices=models.JSONField(default=dict,blank=True)
    correct_choices=models.JSONField(default=dict,blank=True)
    # grading
    correct_grade=models.IntegerField(default=0)
    incorrect_penalty=models.IntegerField(default=0)

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

class StudentAnswer(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    page=models.ForeignKey(CoursePage,on_delete=models.CASCADE)
    ANSWER_TYPE = (
        ('N',None),
        ('T','Text'),
        ('S','Singular Choice'),
        ('M','Multiple Choice'),
        ('F','File Upload'),
    )
    answer_type=models.CharField(max_length=1,choices=ANSWER_TYPE,default='N') #for nuking non-matching responses
    class Meta:
        abstract=True
class StudentAnswerText(StudentAnswer):
    response=models.TextField(default='',blank=True)
    def __str__(self):
        return 'Answer of '+str(self.user)+' for '+str(self.page)
class StudentAnswerFile(StudentAnswer):
    response=models.FileField(default=None,upload_to='user_responses/',null=True,blank=True)
    def __str__(self):
        return 'File Answer of '+str(self.user)+' for '+str(self.page)

class UserPerms(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    is_teacher=models.BooleanField(default=False) #can create courses, groups
    is_manager=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username+'\'s permissions'
    
class UserGroups(models.Model):
    name=models.CharField(max_length=100)
    teacher=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    def save(self,*args,**kwargs):
        self.name=self.name.replace('/','').replace('?','')
        super(UserGroups,self).save(*args,**kwargs)
    def __str__(self):
        return self.name+' group of '+self.teacher.username

class GroupEnrollment(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    group=models.ForeignKey(UserGroups,on_delete=models.CASCADE)

    def __str__(self):
        return self.student.username+' in '+self.group.name

class GroupAssignments(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    group=models.ForeignKey(UserGroups,on_delete=models.CASCADE)
    deadline=models.DateTimeField(null=True,default=None,blank=True)

    def __str__(self):
        return self.course.name+' in '+self.group.name

class CurrentPageControl(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    page=models.ForeignKey(CoursePage,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.CASCADE)

class Notifications(models.Model):
    group=models.ForeignKey(UserGroups,on_delete=models.CASCADE)
    title=models.TextField(default='')
    text=models.TextField(default='')
    read=models.ManyToManyField(User,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserPFP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pfp=models.ImageField(null=True,blank=True,upload_to='user_pfps/')
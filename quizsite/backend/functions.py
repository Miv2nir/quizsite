import json 



from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

def find_courses(prompt=''):
    if not prompt:
        lookup=models.Course.objects.filter(access='A')
    else:
        lookup=models.Course.objects.filter(access='A',name__contains=prompt)
    return lookup
'''
def define_answer_old(course_page_obj,form_answer_type,a_choices={}):
    #Creates an answer type for the course page object with the definition of choices and types based on the input of form_answer_type
    #returns either a None (when no new object is being made) or the object itself
    #assuming that the function gets an old course_page_obj, before writing a respective field
    print(course_page_obj.answer_type,form_answer_type)
    if course_page_obj.answer_type != form_answer_type: #page answer type has changed
        if course_page_obj.answer_type!='N': #delete the old object if it exists
            try:
                models.PageAnswerText.objects.filter(page=course_page_obj)[0].delete()
            except IndexError: #in case there was an exception and the course page didnt get a chance to change its attribute
                pass
        #making a new one
        if form_answer_type=='N': #do not make anything new
            answer_type_obj=None
        elif form_answer_type=='T':
            answer_type_obj=models.PageAnswerText(page=course_page_obj)
        elif form_answer_type=='F':
            raise NotImplementedError
        else:
            answer_type_obj=models.PageAnswerText(page=course_page_obj,choices=a_choices)
            answer_type_obj.is_choice=True
            if form_answer_type=='M':
                answer_type_obj.is_multiple=True
            print('choices define answer:',answer_type_obj.choices)
        try:
            answer_type_obj.save()
        except AttributeError:
            pass
    else: #no changes were made, grab the object and go
        if course_page_obj.answer_type=='N':
            answer_type_obj=None
        elif course_page_obj.answer_type=='F':
            raise NotImplementedError
        else:
            answer_type_obj=models.PageAnswerText.objects.filter(page=course_page_obj)[0]
    print('choices 2:',answer_type_obj.choices)
    return answer_type_obj
    #1. None to something: create new object
    #2. Something to something
    #3. Something to none
'''
#TODO Sort these functions out so that it wouldn't go yandere sim mode like last year
#I imagine that the auth will have to be served by django/passed through vue without much change
def to_paired_tuples(l):
    '''makes a set of paired tuples of answer choices and empty data as fsr the multiplechoice widget refuses to accept lists'''
    r_tuples=[]
    for i in l:
        r_tuples.append((i,''))
    return tuple(r_tuples)
def clear_answers(course_page_obj,form_answer_type): #void
    '''if a change is done to the answer type, invalidate (aka remove) all of the user given answers as they would no longer be valid'''
    print(course_page_obj.answer_type,form_answer_type)
    if course_page_obj.answer_type==form_answer_type:
        print('not deleting anything')
        return True
    else:
        print(course_page_obj.answer_type in ['N','T','S','M'])
        if course_page_obj.answer_type in ['N','T','S','M']: #text data
            lookup=models.StudentAnswerText.objects.filter(answer_type=course_page_obj.answer_type,page=course_page_obj)
            print(lookup)
            for i in lookup:
                print('deleting',i)
                i.delete()
        #TODO: deletion for files after they're done
        return True

def define_answer(course_page_obj,form_answer_type,a_choices={},c_choices={},a_text="",grade=0,penalty=0):
    '''
    Creates an answer type for the course page object with the definition of choices and types based on the input of form_answer_type
    returns either a None (when no new object is being made) or the object itself
    '''
    print(course_page_obj.answer_type,form_answer_type)
    try:
        answer_type_obj=models.PageAnswerText.objects.filter(page=course_page_obj)[0]
        if answer_type_obj.choices=="":
            answer_type_obj.choices=a_choices
        if answer_type_obj.correct_choices=="":
            answer_type_obj.correct_choices=c_choices
        if answer_type_obj.text=="":
            answer_type_obj.text=a_text
    except IndexError:
        answer_type_obj=models.PageAnswerText(page=course_page_obj,choices=a_choices,correct_choices=c_choices,text=a_text)
    #defining the thing
    #if form_answer_type=='N': #do not make anything new
    #    answer_type_obj.is_choice=False
    #    answer_type_obj.is_multiple=False
    if form_answer_type in ['T','N']: #for non-destructive saving
        #answer_type_obj=models.PageAnswerText(page=course_page_obj)
        answer_type_obj.is_choice=False
        answer_type_obj.is_multiple=False
        answer_type_obj.is_file=False
        #answer_type_obj.text=a_text
    elif form_answer_type=='F':
        answer_type_obj.is_choice=False
        answer_type_obj.is_multiple=False
        answer_type_obj.is_file=True
    else:
        #answer_type_obj=models.PageAnswerText(page=course_page_obj,choices=a_choices)
        answer_type_obj.is_choice=True
        if form_answer_type=='M':
            answer_type_obj.is_multiple=True
        else:
            answer_type_obj.is_multiple=False
        print('choices define answer:',answer_type_obj.choices)
        if a_choices!={} or course_page_obj==form_answer_type:
            answer_type_obj.choices=a_choices
        if c_choices!={} or course_page_obj==form_answer_type:
            answer_type_obj.correct_choices=c_choices
        if a_text!="" or course_page_obj==form_answer_type:
            answer_type_obj.text=a_text
        print(c_choices=="{}" , form_answer_type=='S' , a_choices!={})
        if c_choices=="{}" and form_answer_type=='S' and a_choices!="{}": #if singular undefined correct response, set it to the first value
            pos=list(json.loads(a_choices).keys())[0]
            #print(json.loads(a_choices)['0'])
            #print(list(json.loads(a_choices).keys())[0])
            substitute_answer={pos:json.loads(a_choices)[str(pos)]}
            print(json.dumps(substitute_answer))
            answer_type_obj.correct_choices=json.dumps(substitute_answer)
    #grades
    answer_type_obj.correct_grade=grade
    answer_type_obj.incorrect_penalty=penalty
    try:
        answer_type_obj.save()
    except AttributeError:
        pass
    return answer_type_obj

#utility function
def move_back_pages(page_number,course_obj):
    lookup=models.CoursePage.objects.filter(parent=course_obj)
    for i in lookup:
        if i.number>=page_number:
            i.number-=1
            i.save()
            print(i.number-1)
        else:
            print(i.number)


#decorator for permissions check
def perm_groups_check(view_func):
    def wrapped(request,*args,**kwargs):
        #print('hello from a decorator!')
        try:
            lookup_perms=models.UserPerms.objects.filter(user=request.user)[0]
        except IndexError:
            lookup_perms=models.UserPerms(user=request.user,is_teacher=False)
        if not lookup_perms.is_teacher:
            raise PermissionDenied
        return view_func(request,*args,**kwargs)
    return wrapped
    '''
    try:
        lookup_perms=models.UserPerms.objects.filter(user=request.user)[0]
    except IndexError:
        lookup_perms=models.UserPerms(user=request.user,is_teacher=False)
    if not lookup_perms.is_teacher:
        raise PermissionDenied
    '''

def handle_quiz_redir(course_obj,page_number,page_next,course_name):
    print('course_obj.is_quiz',course_obj.is_quiz)
    if course_obj.is_quiz:
        if page_number == page_next: #end of the quiz
            return HttpResponseRedirect('/courses/'+course_name+'/browse/end/')
        return HttpResponseRedirect('/courses/'+course_name+'/browse/'+str(page_next)+'/')
    return HttpResponseRedirect('/courses/'+course_name+'/browse/'+str(page_number)+'/?success=true')

def get_last_page(course_obj):
    lookup=models.CoursePage.objects.filter(parent=course_obj)
    max_page_num=0
    for i in lookup:
        max_page_num=max(max_page_num,i.number)
    return max_page_num

def get_group_courses(user):
    #check all groups in which a user is enrolled in
    lookup=models.GroupEnrollment.objects.filter(student=user)
    groups=set()
    for i in lookup:
        groups.add(i.group)
    #get all courses assigned to our completion
    courses=set()
    deadlines={}
    for g in groups:
        lookup_courses=models.GroupAssignments.objects.filter(group=g)
        for i in lookup_courses:
            courses.add(i.course)
            try:
                deadlines[i.course]=str(i.deadline.timestamp())
                #print(i.deadline.timestamp())
            except AttributeError:
                pass
    #print(courses)
    return (courses,deadlines)

def course_privacy_check(user,course_obj): #void
    #only the course author is allowed to see the course itself if it's in private
    if course_obj.access=='C':
        if user!=course_obj.author: #private course yet the user is not an author
            raise PermissionDenied
def check_user_group(user,group_obj):
    if models.GroupEnrollment.objects.filter(student=user,group=group_obj):
        return True     
    return False
def calc_answers_group(course_obj,group_obj,page_obj):
    n_answers=0
    for i in models.StudentAnswerText.objects.filter(page=page_obj):
        if models.GroupEnrollment.objects.filter(student=i.user,group=group_obj):
            #print(models.GroupEnrollment.objects.filter(student=i.user,group=group_obj))
            n_answers+=1
    for i in models.StudentAnswerFile.objects.filter(page=page_obj):
        if models.GroupEnrollment.objects.filter(student=i.user,group=group_obj):
            #print(models.GroupEnrollment.objects.filter(student=i.user,group=group_obj))
            n_answers+=1
    return n_answers

def calc_grade(correct_grade,incorrect_penalty,student_answers,correct_answers):
    points=0
    print(correct_grade,incorrect_penalty,student_answers,correct_answers)
    student_answers=json.loads(student_answers)
    correct_answers=json.loads(correct_answers)
    for i in student_answers:
        if i in correct_answers.keys():
            points+=correct_grade
        else:
            points-=incorrect_penalty
    return max(0,points)

def calc_max_points(correct_grade,correct_answers):
    points=0
    correct_answers=json.loads(correct_answers)
    for i in correct_answers.keys():
        points+=correct_grade
    return max(0,points)
import json 
import datetime


from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from django.contrib.auth import authenticate, login, logout

import uuid

from quizsite.settings import MEDIA_URL

from django.contrib.auth.decorators import login_required

# Create your views here.
from backend.functions import *

def register_user(request):  #reused from the past year's course project
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login'].replace('/','')
            try:  # check for existing users
                user = User.objects.get(username=user_login)
                return render(request, 'backend/register.html', {'form': form,'register':False, 'user_found': True})
            except:
                pass  # no existing user found, proceed
            user_password = form.cleaned_data['password']
            if user_password != form.cleaned_data['password_verify']:  # passwords did not match
                return render(request, 'backend/register.html', {'form': form,'register':False, 'password_mismatch': True})
            user_email = form.cleaned_data['email']

            if (not user_login) or (not user_email) or (not user_password):  # in the case of whether some credentials have been skipped
                return render(request, 'backend/register.html', {'form': form,'register':False, 'incomplete_form': True})

            user = User.objects.create_user(user_login, user_email, user_password)
            user.save()  # created the user
            if user is not None:  # login the newly created user
                print('New User Logging in '+user_login)  # for the tests
                login(request, user)
                #create the permissions object
                perm_obj=models.UserPerms(user=user)
                perm_obj.save()
            return HttpResponseRedirect('/')
    else:  # prompt the form
        form = forms.RegisterForm()
        if request.user.is_authenticated:  # if logged in, redirect to the main page
            return HttpResponseRedirect('/')
    return render(request, 'backend/register.html', {'form': form,'register':False})

def login_user(request):
    forward_path=request.GET.get('next','/')
    print(forward_path)
    if request.method == 'POST':  # look for the imports
        form = forms.AuthForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)

            if request.user.is_authenticated:  # if logged in, redirect to the main page
                return HttpResponseRedirect(forward_path)

            if user is not None:  # accept the form and login the user
                print('Logging in '+user_login)  # for the tests
                login(request, user)
                return HttpResponseRedirect(forward_path)
            else:  # failed credentials check
                form = forms.AuthForm()
                return render(request, 'backend/login.html', {'form': form,'register':False, 'failed_login': True,'next':forward_path})
    else:  # prompt the form
        form = forms.AuthForm()
        if request.user.is_authenticated:  # if logged in, redirect to the main page
            return HttpResponseRedirect(forward_path)
    return render(request, 'backend/login.html', {'form': form,'register':False,'next':forward_path})

def logout_user(request):
    if request.user.is_authenticated:
        print('Logging out '+request.user.username)
        logout(request)
    return HttpResponseRedirect('/login/')

#site's landing page
@login_required
def home(request): #same deal as in the assignments page
    courses,deadlines=get_group_courses(request.user)
    public_courses=find_courses('')
    #gather public courses, same as in the course list

    return render (request,'backend/home.html',{'username':request.user,'assignments':courses,'deadlines':deadlines,'courses':public_courses})

@login_required
def userpage(request):
    courses,deadlines=get_group_courses(request.user)
    try:
        access_level=models.UserPerms.objects.filter(user=request.user)[0]
    except IndexError:
        access_level=models.UserPerms(user=request.user)
        access_level.save()
    #count the number of completed courses
    completed_pages={}
    page_counts={}
    for i in models.StudentAnswerText.objects.filter(user=request.user):
        try:
            completed_pages[i.page.parent]+=1
        except KeyError:
            completed_pages[i.page.parent]=1
    for i in models.StudentAnswerFile.objects.filter(user=request.user):
        try:
            completed_pages[i.page.parent]+=1
        except KeyError:
            completed_pages[i.page.parent]=1
    for i in models.Course.objects.filter():
        pages=i.coursepage_set.all()
        page_counts[i]=len(pages)
    #print(completed_pages)
    #print(page_counts)
    count=0
    for i in completed_pages.keys():
        if completed_pages[i]==page_counts[i]:
            count+=1
    #print(count)
    #authored courses
    authored_courses=models.Course.objects.filter(author=request.user)
    return render (request,'backend/user.html',{'courses':list(courses),
    'username':request.user,'deadlines':deadlines,'is_teacher':access_level.is_teacher,'course_count':count,
    'authored_courses':authored_courses})

#TODO: change basis of name to ID
@login_required
def course_list(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            prompt=form.cleaned_data['search']
            return HttpResponseRedirect('/courses/?prompt='+prompt)
        else:
            return HttpResponseRedirect('/courses/')
    form=forms.SearchForm(initial={'search':request.GET.get('prompt','')})
    lookup=find_courses(request.GET.get('prompt',''))
    #print(lookup)
    return render (request,'backend/course_list.html',{'form': form,'username':request.user,'lookup':lookup})

@login_required
def course_item(request,course_name):
    course_obj=models.Course.objects.filter(name=course_name)[0]
    if_owner=request.user==course_obj.author
    course_privacy_check(request.user,course_obj)
    pages=len(models.CoursePage.objects.filter(parent=course_obj))
    return render (request,'backend/course_item.html',{'username':request.user,
    'course_name':course_name,
    'course_description':course_obj.description,
    'owner':if_owner,
    'n_pages':pages,
    'author_name':course_obj.author})

@login_required
def course_browse_redir(request,course_name):
    return HttpResponseRedirect('/courses/'+course_name+'/browse/1')


@login_required
def course_browse(request,course_name,page_number):
    #success query
    confirmation=request.GET.get('success',False)
    #get the course object & page
    course_obj=models.Course.objects.filter(name=course_name)[0]
    try:
        course_page_obj=models.CoursePage.objects.filter(parent=course_obj,number=page_number)[0]
    except IndexError: #no pages yet
        return render(request,'backend/course_browse_no_pages.html',{'user':request.user,'course_name':course_name})
    page_title=course_page_obj.title
    page_text=course_page_obj.text
    
    #navbar values
    try:
        models.CoursePage.objects.filter(parent=course_obj,number=page_number+1)[0]
        page_next=page_number+1
        next_exists=True
    except IndexError:
        page_next=page_number
        next_exists=False
    #page_next=page_number+1
    if page_number == 1:
        page_previous='1'
    else:
        page_previous=page_number-1

    answer_type=course_page_obj.answer_type

    is_quiz=course_obj.is_quiz
    #quiz page control

    try:
        page_control=models.CurrentPageControl.objects.filter(course=course_obj,student=request.user)[0]
        if (page_control.page != course_page_obj) and is_quiz:
            correct_page_num=page_control.page.number
            return HttpResponseRedirect('/courses/'+course_name+'/browse/'+str(correct_page_num))
    except IndexError:
        page_control=models.CurrentPageControl(course=course_obj,student=request.user)
        if course_page_obj.number==1:
            page_control.page=course_page_obj
        else:
            page_control.page=models.CoursePage.objects.filter(parent=course_obj,number=1)[0]
        if is_quiz:
            page_control.save()
    template_values={'username':request.user,'confirmation':confirmation,
    'course_name':course_name,
    'page_title':page_title,
    'page_text':page_text,
    'page_number':page_number,
    'page_previous':page_previous,
    'page_next':page_next,
    'next_exists':next_exists,
    'is_file':answer_type=='F',
    'is_quiz':is_quiz, 'quiz_time':course_page_obj.time,
    'first_page':page_number==1}

    if answer_type=='N': #no answer, proceed with the serving
        #switch the lock to the next page
        page_control.page=models.CoursePage.objects.filter(parent=course_obj,number=page_next)[0]
        page_control.save()
        return render (request,'backend/course_browse.html',template_values)

    answer_type_obj=models.PageAnswerText.objects.filter(page=course_page_obj)[0]
    template_values['question_itself']=answer_type_obj.text #get question text
    try:
        tuple_choices=tuple(json.loads(answer_type_obj.choices).items()) #apparently it's needed to be like that in forms
    except TypeError:
        tuple_choices=tuple()
    if answer_type=='T': #answer_type is text
        #got the form
        if request.method=='POST':
            form=forms.UserResponseText(request.POST)
            if form.is_valid(): #do stuff
                #if the response already exists
                lookup = models.StudentAnswerText.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)
                if lookup:
                    user_response_obj=lookup[0]
                else:
                    user_response_obj=models.StudentAnswerText(page=course_page_obj,user=request.user,answer_type=answer_type)
                user_response_obj.response=form.cleaned_data['user_response']
                user_response_obj.save()
            #switch the lock to the next page
            page_control.page=models.CoursePage.objects.filter(parent=course_obj,number=page_next)[0]
            page_control.save()
            return handle_quiz_redir(course_obj,page_number,page_next,course_name)
        #request is a get
        form=forms.UserResponseText()
        try: #grab existing response and serve in a form
            user_response_obj=models.StudentAnswerText.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)[0]
            form.initial={'user_response':user_response_obj.response}
        except IndexError: #if it does not exist, pass
            pass

    if answer_type=='F': #answer_type is a file
        #got the form
        if request.method=='POST':
            form=forms.UserResponseFile(request.POST,request.FILES)
            #print(form)
            if form.is_valid():
                lookup=models.StudentAnswerFile.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)
                if lookup:
                    user_response_obj=lookup[0]
                else:
                    user_response_obj=models.StudentAnswerFile(page=course_page_obj,user=request.user,answer_type=answer_type)
                print(user_response_obj.response)
                user_response_obj.response.delete(save=True)
                try:
                    user_response_obj.response=form.cleaned_data['user_response']
                    extension=user_response_obj.response.name.split('.')[-1]
                    user_response_obj.response.name='file_'+request.user.username+'_'+str(uuid.uuid4())+'.'+extension
                    user_response_obj.save()         
                except AttributeError: #no file was actually uploaded
                    pass       
                #switch the lock to the next page
                page_control.page=models.CoursePage.objects.filter(parent=course_obj,number=page_next)[0]
                page_control.save()
                return handle_quiz_redir(course_obj,page_number,page_next,course_name)
        form=forms.UserResponseFile()
        try:
            user_response_obj=models.StudentAnswerFile.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)[0]
            form.initial={'user_response':user_response_obj.response}
            if user_response_obj.response:
                template_values['file_name']=user_response_obj.response.name
        except IndexError:
            pass

    if answer_type=='S': #answer_type is singular choice
        #got the form
        if request.method=='POST':
            form=forms.UserResponseSingular(request.POST)
            #validation or something
            user_response=request.POST.get('user_response')
            print(user_response)
            form.fields['user_response'].choices=[(user_response,'')] #fsr the response does not get passed so gotta shove it into the form for the rest to make sense
            print(form.fields['user_response'].choices)
            if form.is_valid(): #do stuff
                #if response already exists
                #same model as choices store text data
                lookup = models.StudentAnswerText.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)
                if lookup:
                    user_response_obj=lookup[0]
                else:
                    user_response_obj=models.StudentAnswerText(page=course_page_obj,user=request.user,answer_type=answer_type)
                user_response_obj.response=form.cleaned_data['user_response']
                user_response_obj.save()
            #switch the lock to the next page
            page_control.page=models.CoursePage.objects.filter(parent=course_obj,number=page_next)[0]
            page_control.save()
            return handle_quiz_redir(course_obj,page_number,page_next,course_name)
        form=forms.UserResponseSingular()
        form.fields['user_response'].choices=tuple(tuple_choices)
        print(form.fields['user_response'].choices)
        try: #grab existing response and serve in a form
            user_response_obj=models.StudentAnswerText.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)[0]
            form.initial={'user_response':user_response_obj.response}
        except IndexError:
            pass 
    if answer_type=='M': #answer_type is multiple choice
        #got the form
        if request.method=='POST':
            form=forms.UserResponseMultiple(request.POST)
            #print(request.POST['user_response'])
            #same validation thing
            #user_response=request.POST.get('user_response')
            #print(user_response)
            #form.fields['user_response'].choices=[(user_response,'')] #fsr the response does not get passed so gotta shove it into the form for the rest to make sense
            #print(form.fields['user_response'].choices)
            user_response=request.POST.getlist('user_response')
            form.fields['user_response'].choices=to_paired_tuples(user_response)
            #form.fields['user_response'].choices=tuple(user_response)
            print(form.errors)
            if form.is_valid(): #do stuff
                #if response already exists
                #same model as choices store text data
                lookup = models.StudentAnswerText.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)
                if lookup:
                    user_response_obj=lookup[0]
                else:
                    user_response_obj=models.StudentAnswerText(page=course_page_obj,user=request.user,answer_type=answer_type)
                user_response_obj.response=form.cleaned_data['user_response']
                user_response_obj.save()
            #switch the lock to the next page
            page_control.page=models.CoursePage.objects.filter(parent=course_obj,number=page_next)[0]
            page_control.save()
            return handle_quiz_redir(course_obj,page_number,page_next,course_name)
        form=forms.UserResponseMultiple()
        print(tuple(tuple_choices))
        form.fields['user_response'].choices=tuple(tuple_choices)
        try: #grab existing response and serve in a form
            user_response_obj=models.StudentAnswerText.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)[0]
            response_list=json.loads(user_response_obj.response.replace("'",'"'))
            for i in response_list:
                print(i)
            #form.initial={'user_response':serialized_list_from_str(user_response_obj.response)}
            form.initial={'user_response':response_list}
        except IndexError:
            pass
    template_values['form']=form

    #temporary fallback
    return render (request,'backend/course_browse.html',template_values)
    #TODO: move the tuple out of the function somewhere else

@login_required
def course_browse_end(request,course_name):
    #page lock operations
    #if the page lock's page is the last one, remove it
    #otherwise, redirect the user back there
    course_obj=models.Course.objects.filter(name=course_name)[0]
    try: #page lock release
        page_control=models.CurrentPageControl.objects.filter(course=course_obj,student=request.user)[0]
        last_page_num=get_last_page(course_obj)
        if last_page_num==page_control.page.number:
            page_control.delete()
        else:
            correct_page_num=page_control.page.number
            return HttpResponseRedirect('/courses/'+course_name+'/browse/'+str(correct_page_num))
    except IndexError:
        pass
    #calculate the results
    answer_sum=0
    answer_max=0
    for i in models.CoursePage.objects.filter(parent=course_obj):
        if i.answer_type in ['S','M']:
            page_answer_obj=models.PageAnswerText.objects.filter(page=i)[0]
            print(i)
            #answer_sum+=max(0,page_answer_obj.correct_grade-page_answer_obj.incorrect_penalty)
            student_answer=models.StudentAnswerText.objects.filter(page=i,user=request.user)[0].response.replace("'",'"')
            if i.answer_type=='S':
                student_answer='["'+student_answer+'"]'
            correct_answer=models.PageAnswerText.objects.filter(page=i)[0].correct_choices
            answer_sum+=calc_grade(page_answer_obj.correct_grade,page_answer_obj.incorrect_penalty,student_answer,correct_answer)
            answer_max+=calc_max_points(page_answer_obj.correct_grade,correct_answer)
    
    return render(request,'backend/course_browse_end.html',{
        'course_name':course_name,'answer_sum':answer_sum,'answer_max':answer_max
    })

@login_required
def course_edit_redir(request,course_name):
    return HttpResponseRedirect('/courses/'+course_name+'/edit/0')

@login_required
@perm_groups_check
def course_edit(request,course_name,page_number=0):
    #metadata page (does not really exist but is a way to fit some general info of the course here)
    page_previous=max(0,page_number-1)
    page_next=page_number+1 #add check for page limit
    course_obj=models.Course.objects.filter(name=course_name)[0]
    #page 0 stuff
    if page_number==0:
        #if the form was submitted waawawa
        if request.method=='POST':
            form=forms.CourseForm(request.POST)
            if not form.is_valid():
                return HttpResponseRedirect('/courses/'+course_obj.name+'/edit/0')

            course_obj.name=form.cleaned_data['name']
            course_obj.description=form.cleaned_data['description']
            course_obj.access=form.cleaned_data['access']
            #course_page_obj.is_quiz=form.cleaned_data['quiz']
            course_obj.save()
            return HttpResponseRedirect('/courses/'+course_obj.name+'/edit/0/')

        #if the page is being requested
        form=forms.CourseForm(initial={'name':course_obj.name,'description':course_obj.description,
        'access':course_obj.access})
        pages=len(models.CoursePage.objects.filter(parent=course_obj))
        return render (request,'backend/course_edit_page0.html',{'username':request.user,'form':form,
        'course_name':course_name,
        'page_number':page_number,
        'page_previous':page_previous,
        'page_next':page_next,
        'n_pages':pages,
        'is_quiz':course_obj.is_quiz,
        'course_access':course_obj.get_access_display()})

    #content pages
    #TODO: page deleter
    if request.GET.get('create')=='1': #making a new page
        print('making a new page')
        course_page_obj=models.CoursePage()
        course_page_obj.parent=course_obj
        course_page_obj.number=page_number
        course_page_obj.save()
    try:
        course_page_obj=models.CoursePage.objects.filter(parent=course_obj,number=page_number)[0]
    except: #no page created yet
        return render (request,'backend/course_edit_empty.html',{'username':request.user,
    'course_name':course_obj.name,
    'page_number':page_number,
    'page_previous':page_previous})

    #page information update
    if request.method=='POST':
        form=forms.CoursePageForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/courses/'+course_obj.name+'/edit/'+str(page_number)+'/')
        #get the answer object if present
        
        #quiz timer thingy
        course_page_obj.time=form.cleaned_data['timer']

        course_page_obj.title=form.cleaned_data['title']
        course_page_obj.text=form.cleaned_data['text']
        #print('aaaaaaaaaaaaaaaaaaaa')
        
        #time to handle the answer type model
        #choices={0:'Choice 1',1:'Choice 2',2:'Choice 3'} #get as json from client somehow
        choices=form.cleaned_data['choices']
        if not choices:
            choices={}
        #print('choices:',json.dumps(choices))
        correct_choices=form.cleaned_data['correct_choices']
        if not correct_choices:
            correct_choices={}
        print(correct_choices)
        q_text=form.cleaned_data['question']
        if not q_text:
            q_text=""
        #on change of the answer type: delete all of the given answers to that question
        grade=form.cleaned_data['grade']
        if not grade:
            grade=0
        penalty=form.cleaned_data['penalty']
        if not penalty:
            penalty=0
        clear_answers(course_page_obj,form.cleaned_data['answer_type'])
        answer_type_obj=define_answer(course_page_obj,form.cleaned_data['answer_type'],a_choices=choices,
        c_choices=correct_choices,a_text=q_text,grade=grade,penalty=penalty)
        #choices=answer_type_obj.choices

        course_page_obj.answer_type=form.cleaned_data['answer_type']
        course_page_obj.save()

        return HttpResponseRedirect('/courses/'+course_obj.name+'/edit/'+str(page_number)+'/')
    #come up with some choices as an example, should change it to prompting the user later on
    #if answer_type_obj:
        #form_answer_type=forms.AnswerTypeForm(initial={'question':answer_type_obj.text,'choices':answer_type_obj.choices})
    #else:
    #    form_answer_type=None
    try:
        answer_type_obj=models.PageAnswerText.objects.filter(page=course_page_obj)[0]
    except:
        answer_type_obj=models.PageAnswerText(page=course_page_obj,choices={},correct_choices={})
        answer_type_obj.save()
    form=forms.CoursePageForm(initial={'title':course_page_obj.title,
    'text':course_page_obj.text,
    'answer_type':course_page_obj.answer_type,
    'question':answer_type_obj.text,
    'choices':answer_type_obj.choices,
    'correct_choices':answer_type_obj.correct_choices,
    'timer':course_page_obj.time,'grade':answer_type_obj.correct_grade,'penalty':answer_type_obj.incorrect_penalty})

    if course_obj.is_quiz:
        A_TYPE_QUIZ = (
        ('S','Singular Choice'),
        ('M','Multiple Choice'),
    )
        form.fields['answer_type'].choices=A_TYPE_QUIZ
    
    return render (request,'backend/course_edit.html',{'username':request.user,'form':form,
    'course_name':course_obj.name,
    'page_number':page_number,
    'page_previous':page_previous,
    'page_next':page_next,
    'option_type':course_page_obj.answer_type,
    'question_presence':course_page_obj.answer_type!='N',
    'is_quiz':course_obj.is_quiz,
    'choice_type':course_page_obj.answer_type in ['S','M']})
    
@login_required
@perm_groups_check
def course_page_manager(request,course_name):
    course_obj=models.Course.objects.filter(name=course_name)[0]
    pages=models.CoursePage.objects.filter(parent=course_obj)
    n_pages=len(pages)
    return render (request,'backend/course_page_manager.html',{'course_name':course_name,"n_pages":n_pages,'pages':pages})


@login_required
@perm_groups_check
def course_page_manager_delete(request,course_name,page_number):
    course_obj=models.Course.objects.filter(name=course_name)[0]
    page_obj=models.CoursePage.objects.filter(parent=course_obj,number=page_number)[0]
    #grab additional info for the thing
    confirmation=request.GET.get('confirm',False)
    if confirmation: #delete everything and redirect
        #print(confirmation)
        page_obj.save()
        page_obj.delete()
        move_back_pages(page_number,course_obj)
        return HttpResponseRedirect('/courses/'+course_name+'/edit/pages/')
    #TODO: implement file upload counting
    given_answers=models.StudentAnswerText.objects.filter(page=page_obj)
    return render(request,'backend/course_page_manager_delete.html',{'course_name':course_name,'page_obj':page_obj,'page_number':page_number,'n_answers':len(given_answers)})

@login_required
@perm_groups_check
def course_create(request):
    #can access the creation util
    if request.method=='POST':
        form=forms.CourseForm(request.POST)
        if form.is_valid():
            course_obj=models.Course(author=request.user)
            try:
                lookup=models.Course.objects.filter(name=form.cleaned_data['name'])[0]
                return HttpResponseRedirect('/courses/create/?name_collision=True')
            except IndexError:
                pass
            course_obj.name=form.cleaned_data['name']
            course_obj.description=form.cleaned_data['description']
            course_obj.access=form.cleaned_data['access']
            course_obj.is_quiz=form.cleaned_data['quiz']
            course_obj.save()
            return HttpResponseRedirect('/courses/'+course_obj.name+'/edit/0/?new=True')
    form=forms.CourseForm()
    return render(request,'backend/course_create.html',{'form':form})

@login_required
@perm_groups_check
def course_delete(request,course_name):
    course_obj=models.Course.objects.filter(name=course_name)[0]
    confirmation=request.GET.get('confirm',False)
    if confirmation:
        course_obj.delete()
        return HttpResponseRedirect('/courses/')
    n_pages=len(models.CoursePage.objects.filter(parent=course_obj))
    return render(request,'backend/course_delete.html',{'course_obj':course_obj,
    'course_name':course_name,
    'n_pages':n_pages})

@login_required
@perm_groups_check
def group_create(request):
    #can access the creation util
    if request.method=='POST':
        form=forms.UserGroupsForm(request.POST)
        if form.is_valid():
            group_obj=models.UserGroups(teacher=request.user)
            try:
                lookup=models.UserGroups.objects.filter(name=form.cleaned_data['name'])[0]
                return HttpResponseRedirect('/groups/create/?name_collision=True')
            except IndexError:
                pass
            group_obj.name=form.cleaned_data['name']
            group_obj.save()
            return HttpResponseRedirect('/groups/'+group_obj.name+'/?new=True')
    form=forms.UserGroupsForm()
    return render(request,'backend/group_create.html',{'form':form})

@login_required
def group_redir(request,group_name):
    return HttpResponseRedirect('/groups/'+group_name+'/edit/')

@login_required
@perm_groups_check
def group_edit(request,group_name):
    #permissions check
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    if group_obj.teacher!=request.user:
        raise PermissionDenied
    #can access the creation util
    if request.method=='POST':
        form=forms.UserGroupsForm(request.POST)
        if form.is_valid():
            group_obj=models.UserGroups(teacher=request.user)
            try:
                lookup=models.UserGroups.objects.filter(name=form.cleaned_data['name'])[0]
                return HttpResponseRedirect('/groups/create/?name_collision=True')
            except IndexError:
                pass
            group_obj.name=form.cleaned_data['name']
            group_obj.save()
            return HttpResponseRedirect('/groups/'+group_obj.name+'/?new=True')
    form=forms.UserGroupsForm(initial={'name':group_name})
    return render(request,'backend/group_edit.html',{'form':form,'group_name':group_obj.name})
    
@login_required
@perm_groups_check
def group_students(request,group_name):
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    if group_obj.teacher!=request.user:
        raise PermissionDenied
    if request.method=="POST": #forceful student enrollment lol
        form=forms.UserGet(request.POST)
        if form.is_valid():
            #find the user
            try:
                user_obj=models.User.objects.filter(username=form.cleaned_data['username'])[0]
                try:
                    enrollment_obj=models.GroupEnrollment.objects.filter(student=user_obj,group=group_obj)[0]
                    return HttpResponseRedirect('/groups/'+group_obj.name+'/students/?already_enrolled=True')
                except IndexError:
                    enrollment_obj=models.GroupEnrollment(student=user_obj,group=group_obj)
                    enrollment_obj.save()
                    #exits the thing
            except IndexError:
                return HttpResponseRedirect('/groups/'+group_obj.name+'/students/?user_not_found=True')
            return HttpResponseRedirect('/groups/'+group_obj.name+'/students/?success=True')

    form=forms.UserGet()
    #build a list of enrolled students
    enrolled_list=models.GroupEnrollment.objects.filter(group=group_obj)
    return render(request,'backend/group_students.html',{'group_name':group_obj.name,'form':form,'enrolled_list':enrolled_list})

@login_required
def group_students_delete_redir(request,group_name):
    return HttpResponseRedirect('/groups/'+group_name+'/students/')

@login_required
@perm_groups_check
def group_students_delete(request,group_name,student_name):
    user_obj=models.User.objects.filter(username=student_name)[0]
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    enrollment_obj=models.GroupEnrollment.objects.filter(student=user_obj,group=group_obj)[0]
    confirmation=request.GET.get('confirm',False)
    if confirmation:
        enrollment_obj.delete()
        return HttpResponseRedirect('/groups/'+group_name+'/students/')
    return render(request,'backend/group_student_delete.html',{'group_name':group_name,'student_name':student_name})

@login_required
@perm_groups_check
def group_assignments(request,group_name):
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    if group_obj.teacher!=request.user:
        raise PermissionDenied
    if request.method=="POST":
        form=forms.CourseGet(request.POST)
        if form.is_valid():
            try:
                course_obj=models.Course.objects.filter(name=form.cleaned_data['course'])[0]
                try:
                    assignment_obj=models.GroupAssignments.objects.filter(group=group_obj,course=course_obj)[0]
                    return HttpResponseRedirect('/groups/'+group_name+'/assignments/?already_added=True')
                except IndexError:
                    assignment_obj=models.GroupAssignments(group=group_obj,course=course_obj)
                    assignment_obj.save()
            except IndexError:
                return HttpResponseRedirect('/groups/'+group_name+'/assignments/?course_not_found=True')
            return HttpResponseRedirect('/groups/'+group_name+'/assignments/?success=True')
        
    form=forms.CourseGet()
    courses=find_courses('')
    assignments_list=models.GroupAssignments.objects.filter(group=group_obj)
    return render(request,'backend/group_assignments.html',{'group_name':group_name,'form':form,'assignments_list':assignments_list,'courses':courses})

@login_required
def group_assignments_delete_redir(request,group_name):
    return HttpResponseRedirect('/groups/'+group_name+'/assignments/')

@login_required
@perm_groups_check
def group_assignments_delete(request,group_name,course_name):
    course_obj=models.Course.objects.filter(name=course_name)[0]
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    assignment_obj=models.GroupAssignments.objects.filter(group=group_obj,course=course_obj)[0]
    confirmation=request.GET.get('confirm',False)
    if confirmation:
        assignment_obj.delete()
        return HttpResponseRedirect('/groups/'+group_name+'/assignments/')
    return render(request,'backend/group_assignments_delete.html',{'group_name':group_name,'course_name':course_name})

@login_required
@perm_groups_check
def group_notifications(request,group_name):
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    #making a new notification
    delete=request.GET.get('delete',False)
    if delete:
        notif_obj=models.Notifications.objects.get(pk=int(delete))
        notif_obj.delete()
        #return HttpResponseRedirect('/groups/'+group_name+'/notifications/')
    if request.method=="POST":
        form=forms.NotificationForm(request.POST)
        if form.is_valid():
            notif_obj=models.Notifications()
            notif_obj.title=form.cleaned_data['title']
            notif_obj.text=form.cleaned_data['text']
            notif_obj.group=group_obj
            notif_obj.save()
        return HttpResponseRedirect('/groups/'+group_obj.name+'/notifications/')

    notifications=[]
    for j in models.Notifications.objects.filter(group=group_obj):
        notifications.append(j)
    notifications.reverse()
    print(notifications)
    form=forms.NotificationForm()
    return render(request,'backend/group_notifications_manager.html',{'form':form,'group_name':group_name,'notifications':notifications})

@login_required
@perm_groups_check
def group_assignments_item(request,group_name,course_name):
    course_obj=models.Course.objects.filter(name=course_name)[0]
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    assignment_obj=models.GroupAssignments.objects.filter(group=group_obj,course=course_obj)[0]
    n_answers=0
    n_pages=len(models.CoursePage.objects.filter(parent=course_obj))
    participants=set()
    for i in models.CoursePage.objects.filter(parent=course_obj):
        #n_answers+=len(models.StudentAnswerText.objects.filter(page=i))
        #n_answers+=len(models.StudentAnswerFile.objects.filter(page=i))
        n_answers+=calc_answers_group(course_obj,group_obj,i)
        #construct a list of all users who posted answers
        for j in models.StudentAnswerText.objects.filter(page=i):
            if check_user_group(j.user,group_obj):
                participants.add(j.user)
        for j in models.StudentAnswerFile.objects.filter(page=i):
            if check_user_group(j.user,group_obj):
                participants.add(j.user)
    print(participants)
    #set deadlines
    if request.method=="POST":
        form=forms.AssignmentDeadlines(request.POST)
        if form.is_valid():
            assignment_obj.deadline=form.cleaned_data['deadline']
            assignment_obj.save()
        return HttpResponseRedirect('/groups/'+group_obj.name+'/assignments/'+course_name+'/?success=true')
    #generate time difference
    try:
        deadline=assignment_obj.deadline.timestamp
    except AttributeError:
        deadline=None
    form=forms.AssignmentDeadlines(initial={'deadline':assignment_obj.deadline})    
    return render(request,'backend/group_assignments_item.html',{'group_name':group_name,
    'course_name':course_name,'n_answers':n_answers,'n_pages':n_pages,'course_obj':course_obj,
    'participants':participants,'form':form,'deadline':deadline})

#we've finally arrived
@login_required
@perm_groups_check
def group_assignments_user_results(request,group_name,course_name,student_name):
    #get the objects
    course_obj=models.Course.objects.filter(name=course_name)[0]
    group_obj=models.UserGroups.objects.filter(name=group_name)[0]
    user_obj=models.User.objects.filter(username=student_name)[0]
    #get all of user's responses to course pages
    user_answers={}
    correct_answers={}
    answer_types={}
    question_texts={}
    n_pages=0
    answer_texts={}
    answer_points={}
    print(models.CoursePage.objects.filter(parent=course_obj))
    for i in models.CoursePage.objects.filter(parent=course_obj).order_by('number'):
        #user_answer=models.StudentAnswerText.objects.filter(page=i)[0].response
        answer_types[i.number]=i.answer_type
        #print('aaaa',i.answer_type)
        try:
            if answer_types[i.number]=='F':
                user_answers[i.number]=MEDIA_URL+models.StudentAnswerFile.objects.filter(page=i,user=user_obj)[0].response.name
            else:
                user_answers[i.number]=models.StudentAnswerText.objects.filter(page=i,user=user_obj)[0].response.replace("'",'"')
        except IndexError: #must be a null
            user_answers[i.number]="No answer Given"
        if answer_types[i.number]=='S':
            user_answers[i.number]='["'+user_answers[i.number]+'"]'
        correct_answers[i.number]=models.PageAnswerText.objects.filter(page=i)[0].correct_choices
        question_texts[i.number]=models.PageAnswerText.objects.filter(page=i)[0].text
        n_pages+=1
        answer_texts[i.number]=models.PageAnswerText.objects.filter(page=i)[0].choices
        if answer_types[i.number] in ['S','M']: #autograding
            page_answer_obj=models.PageAnswerText.objects.filter(page=i)[0]
            #answer_points[i.number] = max(0,page_answer_obj.correct_grade-page_answer_obj.incorrect_penalty)
            answer_points[i.number]=calc_grade(page_answer_obj.correct_grade,page_answer_obj.incorrect_penalty,user_answers[i.number],correct_answers[i.number])
        else:
            answer_points[i.number]=0
    #print(user_answers)
    #print(correct_answers)
    #print(answer_types)
    #print(answer_points)
    
    #wrangle user_ansers into json objects

    return render(request,'backend/group_assignments_user_results.html',{'group_name':group_name,
    'course_name':course_name,'student_name':student_name,
    'user_answers':user_answers,'correct_answers':correct_answers,'answer_types':answer_types,
    'keys_list':user_answers.keys(),'question_texts':question_texts,'n_pages':n_pages,
    'answer_texts':answer_texts,'answer_points':answer_points})
#https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
@login_required
@perm_groups_check
def group_browse(request):
    group_lookup=models.UserGroups.objects.filter(teacher=request.user)
    #get the amount of added students
    student_count={}
    for i in group_lookup:
        student_count[i]=len(models.GroupEnrollment.objects.filter(group=i))
    return render(request,'backend/group_browse.html',{'group_lookup':group_lookup,'student_count':student_count})

@login_required
@perm_groups_check
def group_delete(request,group_name):
    group_obj=models.UserGroups.objects.filter(name=group_name,teacher=request.user)[0]

    #if we're actually deleting the thing
    confirmation=request.GET.get('confirm',False)
    if confirmation: #delete everything and redirect
        #print(confirmation)
        group_obj.save()
        group_obj.delete()
        return HttpResponseRedirect('/groups/')
    n_assignments=len(models.GroupAssignments.objects.filter(group=group_obj))
    n_students=len(models.GroupEnrollment.objects.filter(group=group_obj))
    return render(request,'backend/group_delete.html',{'group_name':group_name,
    'n_assignments':n_assignments,'n_students':n_students})

@login_required
def assignments_browse(request):
    courses,deadlines=get_group_courses(request.user)
    print(deadlines)
    return render(request,'backend/assignments.html',{'courses':list(courses),'user':request.user,'deadlines':deadlines})

@login_required
def user_settings(request):
    #print(request.FILES)
    user_obj=request.user
    try:
        pfp_obj=models.UserPFP.objects.filter(user=request.user)[0]
    except IndexError:
        pfp_obj=models.UserPFP(user=request.user)
    if request.method=="POST":
        form=forms.UserDetailsForm(request.POST,request.FILES)
        if form.is_valid():
            if request.FILES:
                pfp_obj.pfp.delete(save=True)
            try:
                pfp_obj.pfp=form.cleaned_data['pfp']
                extension=pfp_obj.pfp.name.split('.')[-1]
                #print(extension)
                pfp_obj.pfp.name=request.user.username+'.'+extension
                pfp_obj.save()
            except AttributeError:
                pass
            #deal with the rest of the form
            new_username=form.cleaned_data['username'].replace('/','').replace('?','')
            print('input',new_username)
            if new_username:
                #check if the username is already taken
                try:
                    lookup=User.objects.filter(username=new_username)[0]
                    return HttpResponseRedirect('/user/settings/?username_taken=true')
                except IndexError:
                    pass
                user_obj.username=new_username
            old_password=form.cleaned_data['old_password']
            new_password=form.cleaned_data['password']
            verify_password=form.cleaned_data['password_verify']
            if old_password and new_password and verify_password:
                upd_user=authenticate(request,username=request.user,password=old_password)
                print(upd_user)
                if upd_user is None: #credentials didn't match
                    return HttpResponseRedirect('/user/settings/?wrong_password=true')
                if new_password==verify_password:
                    user_obj.set_password(new_password)
                else:
                    return HttpResponseRedirect('/user/settings/?password_mismatch=true')

            user_obj.save()
            
            return HttpResponseRedirect('/user/settings/?success=true')
        return HttpResponseRedirect('/user/settings/')

    form=forms.UserDetailsForm()
    return render(request,'backend/settings.html',{'user':request.user,'form':form,
    'pfp':pfp_obj.pfp})

@login_required
def notifications(request):
    notifications=[]
    #show_all= request.GET.get('all',False) #ignore the read field
    show_all=True
    reads={}
    print(show_all)
    for i in models.GroupEnrollment.objects.filter(student=request.user):
        group_obj=i.group
        for j in models.Notifications.objects.filter(group=group_obj):
            reads[j]=True
            if request.user not in j.read.all():
                reads[j]=False
                j.read.add(request.user)
                j.save()
                if not show_all: #render only the unread
                    notifications.append(j)
            if show_all: #render all of them
                notifications.append(j)

            print(j.read.all())
            #mark all as read
    notifications.reverse()
    print(reads)
    return render(request,'backend/notifications.html',{'notifications':notifications,'reads':reads,'show_all':show_all})
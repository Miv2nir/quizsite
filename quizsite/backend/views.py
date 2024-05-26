import json 

from django.shortcuts import render
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# Create your views here.
def find_courses(prompt=''):
    if not prompt:
        lookup=models.Course.objects.filter(access='A')
    else:
        lookup=models.Course.objects.filter(access='A',name__contains=prompt)
    return lookup

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
#TODO Sort these functions out so that it wouldn't go yandere sim mode like last year
#I imagine that the auth will have to be served by django/passed through vue without much change

def define_answer(course_page_obj,form_answer_type,a_choices={}):
    '''
    Creates an answer type for the course page object with the definition of choices and types based on the input of form_answer_type
    returns either a None (when no new object is being made) or the object itself
    '''
    print(course_page_obj.answer_type,form_answer_type)
    try:
        answer_type_obj=models.PageAnswerText.objects.filter(page=course_page_obj)[0]
        if answer_type_obj.choices=="":
            answer_type_obj.choices=a_choices
    except IndexError:
        answer_type_obj=models.PageAnswerText(page=course_page_obj,choices=a_choices)
    #defining the thing
    if form_answer_type=='N': #do not make anything new
        answer_type_obj.is_choice=False
        answer_type_obj.is_multiple=False
    elif form_answer_type=='T':
        #answer_type_obj=models.PageAnswerText(page=course_page_obj)
        answer_type_obj.is_choice=False
        answer_type_obj.is_multiple=False
    elif form_answer_type=='F':
        raise NotImplementedError
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
    try:
        answer_type_obj.save()
    except AttributeError:
        pass
    return answer_type_obj

def register_user(request):  #reused from the past year's course project
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
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
def home(request):
    return render (request,'backend/home.html',{'username':request.user})

@login_required
def userpage(request):
    return render (request,'backend/user.html',{'username':request.user})

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
    #navbar values
    page_next=page_number+1
    if page_number == 1:
        page_previous='1'
    else:
        page_previous=page_number-1
    
    #get the course object & page
    course_obj=models.Course.objects.filter(name=course_name)[0]
    course_page_obj=models.CoursePage.objects.filter(parent=course_obj,number=page_number)[0]
    page_title=course_page_obj.title
    page_text=course_page_obj.text
    #Handle the answer forms
    answer_type=course_page_obj.answer_type
    #1. No answer needed
    template_values={'username':request.user,
    'course_name':course_name,
    'page_title':page_title,
    'page_text':page_text,
    'page_number':page_number,
    'page_previous':page_previous,
    'page_next':page_next}
    if answer_type=='N':
            return render (request,'backend/course_browse.html',template_values)
    #2. Text answer
    if answer_type=='T':
        answer_obj=models.PageAnswerText.objects.filter(page=course_page_obj)[0]
        form=forms.AnswerText()
    #temporary fallback
    return render (request,'backend/course_browse.html',template_values)
    #TODO: move the tuple out of the function somewhere else


@login_required
def course_edit_redir(request,course_name):
    return HttpResponseRedirect('/courses/'+course_name+'/edit/0')

@login_required
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
                return HttpResponseRedirect('/courses/'+course_name+'/edit/0')

            course_obj.name=form.cleaned_data['name']
            course_obj.description=form.cleaned_data['description']
            course_obj.access=form.cleaned_data['access']
            course_obj.save()
            return HttpResponseRedirect('/courses/'+course_obj.name+'/edit/0/')

        #if the page is being requested
        form=forms.CourseForm(initial={'name':course_obj.name,'description':course_obj.description})
        pages=len(models.CoursePage.objects.filter(parent=course_obj))
        return render (request,'backend/course_edit_page0.html',{'username':request.user,'form':form,
        'course_name':course_name,
        'page_number':page_number,
        'page_previous':page_previous,
        'page_next':page_next,
        'n_pages':pages,
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
    'course_name':course_name,
    'page_number':page_number,
    'page_previous':page_previous})

    #page information update
    if request.method=='POST':
        form=forms.CoursePageForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect('/courses/'+course_name+'/edit/'+str(page_number)+'/')
        #get the answer object if present
        
        course_page_obj.title=form.cleaned_data['title']
        course_page_obj.text=form.cleaned_data['text']
        #time to handle the answer type model
        #choices={0:'Choice 1',1:'Choice 2',2:'Choice 3'} #get as json from client somehow
        choices=form.cleaned_data['choices']
        if not choices:
            choices={}
        print('choices:',json.dumps(choices))
        answer_type_obj=define_answer(course_page_obj,form.cleaned_data['answer_type'],a_choices=choices)
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
        answer_type_obj=models.PageAnswerText(page=course_page_obj,choices={})
        answer_type_obj.save()
    form=forms.CoursePageForm(initial={'title':course_page_obj.title,
    'text':course_page_obj.text,
    'answer_type':course_page_obj.answer_type,
    'question':answer_type_obj.text,
    'choices':answer_type_obj.choices})
    
    #form_answer_type=forms.
    return render (request,'backend/course_edit.html',{'username':request.user,'form':form,
    'course_name':course_name,
    'page_number':page_number,
    'page_previous':page_previous,
    'page_next':page_next,
    'option_type':course_page_obj.answer_type,
    'choice_type':course_page_obj.answer_type in ['S','M']})
    
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

def define_answer(course_page_obj,form_answer_type,a_choices={},c_choices={},a_text=""):
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
        #answer_type_obj.text=a_text
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
    
    #get the course object & page
    course_obj=models.Course.objects.filter(name=course_name)[0]
    course_page_obj=models.CoursePage.objects.filter(parent=course_obj,number=page_number)[0]
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
    #1. No answer needed
    template_values={'username':request.user,
    'course_name':course_name,
    'page_title':page_title,
    'page_text':page_text,
    'page_number':page_number,
    'page_previous':page_previous,
    'page_next':page_next,
    'next_exists':next_exists,
    'first_page':page_number==1}

    if answer_type=='N': #no answer, proceed with the serving
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
            return HttpResponseRedirect('/courses/'+course_name+'/browse/'+str(page_number)+'/')
        #request is a get
        form=forms.UserResponseText()
        try: #grab existing response and serve in a form
            user_response_obj=models.StudentAnswerText.objects.filter(page=course_page_obj,user=request.user,answer_type=answer_type)[0]
            form.initial={'user_response':user_response_obj.response}
        except IndexError: #if it does not exist, pass
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
            return HttpResponseRedirect('/courses/'+course_name+'/browse/'+str(page_number)+'/')
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
            return HttpResponseRedirect('/courses/'+course_name+'/browse/'+str(page_number)+'/')
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
        #print('choices:',json.dumps(choices))
        correct_choices=form.cleaned_data['correct_choices']
        if not correct_choices:
            correct_choices={}
        print(correct_choices)
        q_text=form.cleaned_data['question']
        if not q_text:
            q_text=""
        #on change of the answer type: delete all of the given answers to that question
        clear_answers(course_page_obj,form.cleaned_data['answer_type'])
        answer_type_obj=define_answer(course_page_obj,form.cleaned_data['answer_type'],a_choices=choices,c_choices=correct_choices,a_text=q_text)
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
    'correct_choices':answer_type_obj.correct_choices,})
    
    return render (request,'backend/course_edit.html',{'username':request.user,'form':form,
    'course_name':course_name,
    'page_number':page_number,
    'page_previous':page_previous,
    'page_next':page_next,
    'option_type':course_page_obj.answer_type,
    'question_presence':course_page_obj.answer_type!='N',
    'choice_type':course_page_obj.answer_type in ['S','M']})
    
@login_required
def course_page_manager(request,course_name):
    course_obj=models.Course.objects.filter(name=course_name)[0]
    pages=models.CoursePage.objects.filter(parent=course_obj)
    n_pages=len(pages)
    return render (request,'backend/course_page_manager.html',{'course_name':course_name,"n_pages":n_pages,'pages':pages})

def move_back_pages(page_number,course_obj):
    lookup=models.CoursePage.objects.filter(parent=course_obj)
    for i in lookup:
        if i.number>=page_number:
            i.number-=1
            i.save()
            print(i.number-1)
        else:
            print(i.number)

@login_required
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
    return render (request,'backend/course_page_manager_delete.html',{'course_name':course_name,'page_obj':page_obj,'page_number':page_number,'n_answers':len(given_answers)})
    
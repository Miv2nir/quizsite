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


#TODO Sort these functions out so that it wouldn't go yandere sim mode like last year
#I imagine that the auth will have to be served by django/passed through vue without much change

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
    return render (request,'backend/course_item.html',{'username':request.user,'course_name':course_name})

@login_required
def course_browse_redir(request,course_name):
    return HttpResponseRedirect('/courses/'+course_name+'/browse/1')

@login_required
def course_browse(request,course_name,page_number):
    page_next=page_number+1
    if page_number == 1:
        page_previous='1'
    else:
        page_previous=page_number-1
    return render (request,'backend/course_browse.html',{'username':request.user,
    'course_name':course_name,
    'page_number':page_number,
    'page_previous':page_previous,
    'page_next':page_next})

@login_required
def course_edit_redir(request,course_name):
    return HttpResponseRedirect('/courses/'+course_name+'/edit/0')

@login_required
def course_edit(request,course_name,page_number=0):
    if page_number==0:
        lookup=find_courses()
        form=forms.CourseForm(initial={'name'})
        return render (request,'backend/course_edit_page0.html',{'username':request.user,
    'course_name':course_name,
    'page_number':page_number})
    return render (request,'backend/course_edit.html',{'username':request.user,
    'course_name':course_name,
    'page_number':page_number})
    
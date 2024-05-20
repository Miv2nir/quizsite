from django.shortcuts import render
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import backend.forms as forms
import backend.models as models
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def find_courses(prompt=''):
    if not prompt:
        lookup=models.Course.objects.filter()
    else:
        lookup=models.Course.objects.filter(access='A',name__unaccent__icontains=prompt)
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
    if request.method == 'POST':  # look for the imports
        form = forms.AuthForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)

            if request.user.is_authenticated:  # if logged in, redirect to the main page
                return HttpResponseRedirect('/')

            if user is not None:  # accept the form and login the user
                print('Logging in '+user_login)  # for the tests
                login(request, user)
                return HttpResponseRedirect('/')
            else:  # failed credentials check
                form = forms.AuthForm()
                return render(request, 'backend/login.html', {'form': form,'register':False, 'failed_login': True})
    else:  # prompt the form
        form = forms.AuthForm()
        if request.user.is_authenticated:  # if logged in, redirect to the main page
            return HttpResponseRedirect('/')
    return render(request, 'backend/login.html', {'form': form,'register':False})


def logout_user(request):
    if request.user.is_authenticated:
        print('Logging out '+request.user.username)
        logout(request)
    return HttpResponseRedirect('/login/')


#site's landing page
def home(request):
    if not request.user.is_authenticated:
        #if the user is not authenticated, redirect to the login page
        return HttpResponseRedirect('/login/')
    return render (request,'backend/home.html',{'username':request.user})

def userpage(request):
    if not request.user.is_authenticated:
        #if the user is not authenticated, redirect to the login page
        return HttpResponseRedirect('/login/')
    return render (request,'backend/user.html',{'username':request.user})
def course_list(request):
    if not request.user.is_authenticated:
        #if the user is not authenticated, redirect to the login page
        return HttpResponseRedirect('/login/')
    form=forms.SearchForm()
    lookup=find_courses()
    print(lookup)
    return render (request,'backend/course_list.html',{'form': form,'username':request.user,'lookup':lookup})
def course_item(request,course_name):
    if not request.user.is_authenticated:
        #if the user is not authenticated, redirect to the login page
        return HttpResponseRedirect('/login/')
    return render (request,'backend/course_item.html',{'username':request.user,'course_name':course_name})
def course_browse_redir(request,course_name):
    if not request.user.is_authenticated:
        #if the user is not authenticated, redirect to the login page
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/courses/'+course_name+'/browse/1')
def course_browse(request,course_name,page_number):
    if not request.user.is_authenticated:
        #if the user is not authenticated, redirect to the login page
        return HttpResponseRedirect('/login/')
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
    
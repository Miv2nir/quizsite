"""
URL configuration for quizsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend import views
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from django.conf.urls.static import static

urlpatterns = [
        re_path(
        r'^statics/(?P<path>.*)$',
        serve,
        {
            'document_root': settings.STATIC_URL,
            'show_indexes': True,  # must be True to render file list
        },
    ),
    path('',views.home,name='home_page'),
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('user/', views.userpage, name='userpage'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<str:course_name>/', views.course_item, name='course_item'),
    path('courses/<str:course_name>/delete/', views.course_delete, name='course_delete'),
    path('courses/<str:course_name>/browse/', views.course_browse_redir, name='course_browse_redir'),
    path('courses/<str:course_name>/browse/<int:page_number>/', views.course_browse, name='course_browse'),
    path('courses/<str:course_name>/browse/end/', views.course_browse_end, name='course_browse_end'),
    path('courses/<str:course_name>/edit/', views.course_edit_redir, name='course_edit_redir'),
    path('courses/<str:course_name>/edit/pages/', views.course_page_manager, name='course_page_manager'),
    path('courses/<str:course_name>/edit/pages/delete/<int:page_number>/', views.course_page_manager_delete, name='course_page_manager_delete'),
    path('courses/<str:course_name>/edit/<int:page_number>/', views.course_edit, name='course_edit'),
    path('groups/',views.group_browse,name='group_browse'),
    path('groups/create/',views.group_create,name='group_create'),
    path('groups/<str:group_name>/',views.group_redir,name='group_redir'),
    path('groups/<str:group_name>/edit/',views.group_edit,name='group_edit'),
    path('groups/<str:group_name>/delete/',views.group_delete,name='group_delete'),
    path('groups/<str:group_name>/students/',views.group_students,name='group_students'),
    path('groups/<str:group_name>/students/delete/',views.group_students_delete_redir,name='group_students_delete_redir'),
    path('groups/<str:group_name>/students/delete/<str:student_name>/',views.group_students_delete,name='group_students_delete'),
    path('groups/<str:group_name>/students/delete/',views.group_assignments_delete_redir,name='group_assignments_delete_redir'),
    path('groups/<str:group_name>/assignments/',views.group_assignments,name='group_assignments'),
    path('groups/<str:group_name>/assignments/delete/<str:course_name>/',views.group_assignments_delete,name='group_assignments_delete'),
    path('groups/<str:group_name>/assignments/<str:course_name>/',views.group_assignments_item,name='group_assignments_item'),
    path('groups/<str:group_name>/assignments/<str:course_name>/<str:student_name>/',views.group_assignments_user_results,name='group_assignments_user_results'),
    path('groups/<str:group_name>/notifications/',views.group_notifications,name='group_notifications'),
    path('assignments/',views.assignments_browse,name='assignments_browse'),
    path('user/settings/',views.user_settings,name='user_settings'),
    path('notifications/',views.notifications,name='notifications'),
    path('logout/', views.logout_user, name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

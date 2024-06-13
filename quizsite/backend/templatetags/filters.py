from django import template
from django.template.defaulttags import register
import backend.forms as forms
import backend.models as models
from django.contrib.auth.models import User

from django.conf import settings

register=template.Library()

@register.filter #django template filter TODO: move it out elsewhere
def get_item(dictionary,key):
    return dictionary.get(key)

@register.filter #see perms of the user
def check_teacher(user):
    #user_obj=User.objects.filter(username=username)[0]
    try:
        condition=models.UserPerms.objects.filter(user=user)[0].is_teacher
    except IndexError:
        condition=False
    return condition

@register.filter #see user enrollment in any group
def check_group_enrollment(user):
    lookup=models.GroupEnrollment.objects.filter(student=user)
    if len(lookup)>0:
        return True
    return False

@register.filter #get user pfp
def get_pfp(user):
    try:
        pfp_obj=models.UserPFP.objects.filter(user=user)[0]
        #return settings.MEDIA_ROOT+pfp_obj.pfp
        return pfp_obj.pfp.url
    except IndexError:
        return settings.STATIC_URL+'pfp.png'
    except ValueError:
        return settings.STATIC_URL+'pfp.png'

@register.filter #get the number of unread notifications
def get_notif_number(user):
    #get all the relevant notifications
    count=0
    try:
        for i in models.GroupEnrollment.objects.filter(student=user):
            group_obj=i.group
            for j in models.Notifications.objects.filter(group=group_obj):
                if user not in j.read.all():
                    count+=1
    except IndexError:
        pass
    return count

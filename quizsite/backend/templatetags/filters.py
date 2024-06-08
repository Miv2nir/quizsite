from django import template
from django.template.defaulttags import register
import backend.forms as forms
import backend.models as models
from django.contrib.auth.models import User

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
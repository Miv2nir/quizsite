from django import template
from django.template.defaulttags import register

register=template.Library()

@register.filter #django template filter TODO: move it out elsewhere
def get_item(dictionary,key):
    return dictionary.get(key)
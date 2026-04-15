from django import template

register = template.Library()

@register.filter
def space_split(value):
    return value.split()

@register.filter
def get_item(dictionary, key):
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return None

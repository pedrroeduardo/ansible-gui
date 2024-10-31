from django import template

register = template.Library()


@register.filter
def reverse_list(value):
    return value[::-1]

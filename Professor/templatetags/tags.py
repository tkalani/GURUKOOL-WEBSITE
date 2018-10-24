from django import template

register = template.Library()

@register.assignment_tag
def update_variable(value):
    data = value
    return data
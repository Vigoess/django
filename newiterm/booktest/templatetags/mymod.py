from django.template import Library

register =  Library()

@register.filter
def mod(num1,num2):
    return num1%num2
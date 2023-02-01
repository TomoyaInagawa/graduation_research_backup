from django import template
 
 
register = template.Library()
 
@register.filter
def div(value, args):
    return value // args
    
@register.filter
def rem(value, args):
    return value % args
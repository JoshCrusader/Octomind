from django import template
register = template.Library()
@register.filter(name='times')
def times(n):
    return range(0, n)
from django import template
register = template.Library()
@register.filter(name='attr')
def attr(obj, prop):
    try:
        return obj[prop]
    except:
        return None
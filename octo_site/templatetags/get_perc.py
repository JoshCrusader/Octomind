from django import template
register = template.Library()
@register.filter(name='perc')
def perc(obj, prop):
    if(obj != 0):
        print('im not 0000')
        print(obj)
    try:
        return round((obj/prop * 100))
    except:
        return '0%'
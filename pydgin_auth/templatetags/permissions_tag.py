'''Module to handle permissions tags. Use can use these tags in templates directly'''

from django import template
register = template.Library()


@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    '''
    Usage:
    {% load permissions_tag %}
    {% if user|is_in_group:"DIL" %}
    do something.....
    {% endif %}
    '''
    return user.groups.filter(name=group_name).exists()

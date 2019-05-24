from django import template

register = template.Library()


@register.filter
def filter_scout(value):

    return value.lower()

from django import template
register = template.Library()


@register.filter
def get_item(object, key):
    return getattr(object, key, None)

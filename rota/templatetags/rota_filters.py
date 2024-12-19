from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Custom template filter to get a dictionary item by key.
    """
    return dictionary.get(key)
# apps/app_name/templatetags/custom_filters.py
from django import template

register = template.Library()

# Define your custom filter here
@register.filter(name='add_class')
def add_class(value, class_name):
    return value.as_widget(attrs={'class': class_name})

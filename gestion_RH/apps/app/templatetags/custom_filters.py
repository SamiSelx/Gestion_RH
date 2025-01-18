# apps/app_name/templatetags/custom_filters.py
from django import template
from ..models import FicheDePaieS

register = template.Library()

# Define your custom filter here
@register.filter(name='add_class')
def add_class(value, class_name):
    return value.as_widget(attrs={'class': class_name})

@register.filter(name='get_fiche_by_employe')
def get_fiche_by_employe(value, employe_id):
    return FicheDePaieS.objects.filter(employe__id=employe_id).first()
from django import template
from pricing.models import Project

import pdb

register = template.Library()

@register.filter(name='project_name')
def project_name(value):
    obj = Project.objects.get(pk=value)
    if obj is None:
        return ""
    return obj.name
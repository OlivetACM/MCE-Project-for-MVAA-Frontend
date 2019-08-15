from django.utils.safestring import mark_safe
from django import template

import json

register = template.Library()

#creating a js tag for converting django template varialbe to json string.
@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
from django import template
from django.forms import Form

from ..utils import bootstrapify_form

register = template.Library()

@register.filter(name="bootstrapify")
def bootstrapify(form: Form):
    """
    Applies Bootstrap styling to the given form.
    """
    return bootstrapify_form(form)

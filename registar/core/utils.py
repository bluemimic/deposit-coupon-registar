from typing import Type
from django.forms import CheckboxInput, Form, Select, SelectMultiple


def bootstrapify_form(form: Form, floating: bool = False) -> Form:
    """
    Adds `Bootstrap` classes to form field's instances. Returns form, that was bootstrapified.
    If form is floating, adds required `placeholder` attribute.
    """

    for field in iter(form):
        if isinstance(field.field.widget, CheckboxInput):
            field.field.widget.attrs["class"] = "form-check-input"
        elif isinstance(field.field.widget, (Select, SelectMultiple)):
            field.field.widget.attrs["class"] = "form-select"
        else:
            field.field.widget.attrs["class"] = "form-control"

        if floating:
            field.field.widget.attrs["placeholder"] = " "

        if field.errors:
            field.field.widget.attrs["class"] += " is-invalid"

    return form

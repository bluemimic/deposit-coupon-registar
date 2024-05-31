from typing import Type
from django.forms import CheckboxInput, Form, Select, SelectMultiple

import cv2 
from pyzbar.pyzbar import decode 

class NoBarcodeDetected(Exception):
    pass

class NoBarcodeData(Exception):
    pass


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


def extract_barcode(image):
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    detectedBarcodes = decode(img)

    if not detectedBarcodes:
        raise NoBarcodeDetected("No barcode detected in the image.")

    for barcode in detectedBarcodes:
        if barcode.data == "":
            raise NoBarcodeData("No data found in the barcode.")

        return barcode.data.decode("utf-8") 

"""
Form object for taking form data from the client and handling the multipart translation
into fields and files that can be manipulated on the server.
"""
from django import forms

class PictureForm(forms.Form):
    person_first_name = forms.CharField(max_length=75, required=False)
    person_middle_name = forms.CharField(max_length=75, required=False)
    person_last_name = forms.CharField(max_length=100, required=False)
    dog_name = forms.CharField(max_length=255, required=True)
    attachment = forms.FileField()

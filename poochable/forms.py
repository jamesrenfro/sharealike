from django import forms

class UploadFileForm(forms.Form):
    person_first_name = forms.CharField(max_length=75, required=False)
    person_middle_name = forms.CharField(max_length=75, required=False)
    person_last_name = forms.CharField(max_length=100, required=False)
    dog_name = forms.CharField(max_length=255, required=True)
    attachment = forms.FileField()

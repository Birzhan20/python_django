from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label='Your Age', min_value=1, max_value=120)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)


# class CreateOrder(forms.Form):
#     name = forms.CharField(max_length=100)
#     quantity = forms.IntegerField(label='Quantity', min_value=1, max_value=120)
#     price = forms.IntegerField(label='Price', min_value=1, max_value=120)


def validate_file_name(file: InMemoryUploadedFile)-> None:
    if file.name and "virus" in file.name:
        raise ValidationError("File name should not contain 'virus'")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])

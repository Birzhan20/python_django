from django import forms
from myauth.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("user", "first_name", "last_name", "email", "bio", "image")

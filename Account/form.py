from django import forms
from django.contrib.auth.models import User
from Account.models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','password']

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Profile_Image']




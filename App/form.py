from django import forms
from django.contrib.auth.models import User
from App.models import Work


class WorkUpdate(forms.ModelForm):

    class Meta:
        model = Work
        fields = ['About_Design','Select_Region','Price','Upload_Pictures','Make_Private']
        
        





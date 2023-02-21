from django import forms
from django.contrib.auth.models import User

class SinupForm(forms.Form):
    email = forms.EmailField(max_length=30)
    password = forms.CharField(max_length=20, min_length=8, required=True)
    confirmPass = forms.CharField(max_length=20, min_length=8, required=True)

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import UserModel


class ChangeUserNameForm(forms.Form):
    UserName = forms.CharField(max_length=100,required=True)

from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
username_regex_field = forms.RegexField (
        label = "Username",
        max_length = 30,
        regex = r'^[0-9a-zA-Z\_\w]*$',
        help_text = "Only alphanumeric characters are allowed in the username.",
        error_messages={'invalid': ("This value must contain only letters,numbers and underscores.")}
        )

class UserCreationForm(UserCreationForm):
    username = username_regex_field

class UserChangeForm(UserChangeForm):
    username = username_regex_field

class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

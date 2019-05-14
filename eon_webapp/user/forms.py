from django import forms
from .models import UserModel

username_regex_field = forms.RegexField (
        label = "Username",
        max_length = 30,
        regex = r'^[0-9a-zA-Z\_\w]*$',
        help_text = "Only alphanumeric characters are allowed in the username.",
        error_messages={'invalid': ("This value must contain only letters,numbers and underscores.")}
        )
        
class ChangeUserNameForm(forms.Form):
    UserName = username_regex_field

from django import forms

from .models import UserModel


class ModelViewForm(forms.Form):
    graph_title = forms.CharField(label='Graph title', max_length=30)
    x_axis = forms.CharField(label='X-axis title', max_length=20)
    y_axis = forms.CharField(label='Y-axis title', max_length=20)
    description = forms.CharField(widget=forms.Textarea,label='Description', max_length=100)
    param1 = forms.CharField(label='1st Parameter',max_length=25)
    param2 = forms.CharField(label='2nd Parameter',max_length=25)

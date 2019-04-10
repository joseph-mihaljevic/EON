from django import forms

from .models import UserModel


class ModelSpecifyForm(forms.Form):
    graph_title = forms.CharField(label='Graph title', max_length=30)
    x_axis = forms.CharField(label='X-axis title', max_length=20)
    y_axis = forms.CharField(label='Y-axis title', max_length=20)
    graph_description = forms.CharField(widget=forms.Textarea,label='Description', max_length=100)

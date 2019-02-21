from django import forms

from .models import Forum, Thread, Post

class ForumCreationForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ('name','description')

class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('content','thread')

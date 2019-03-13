from django import forms

from .models import Forum, Thread, Comment

class ForumCreationForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ('topic_name','description')

class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ('thread_name','description')

class CommentCreationForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

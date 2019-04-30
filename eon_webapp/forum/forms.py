from django import forms
from .models import Forum, Thread, Comment, Reply

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
        fields = ('content')

class ReplyCreationForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_content','parent_comment', 'child_comment')

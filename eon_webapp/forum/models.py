from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField
from group.models import Group

# Creation of Forum table which has a topic name, description, and group connections
class Forum(models.Model):
    topic_name = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    # Based on app groups model
    group = models.ForeignKey(Group, null=True, blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.topic_name

# Creation of Thread table which has a name, date posted,
# poster, description, and respected forum that are within
class Thread(models.Model):
    thread_name = models.CharField(max_length=80)
    date=models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)
    def __str__(self):
        return self.thread_name

# Creation of Comment table which has content, respected thread,
# poster, and date
class Comment(models.Model):
    content = RichTextField(max_length=800)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    poster = models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# Creation of Reply table which is pretty much a comment to a comment,
# hence it takes in Comment class. A reply has content, a parent, and a possible child
class Reply(Comment):
    reply_content = models.TextField(max_length=800, null = True)
    parent_comment = models.ForeignKey(Comment, blank=False, related_name='comment_parent',on_delete=models.CASCADE)
    child_comment = models.ForeignKey(Comment, blank=True, null=True, related_name='comment_sibling', on_delete=models.CASCADE)

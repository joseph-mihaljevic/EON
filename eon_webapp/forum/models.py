from django.db import models
from django.contrib.auth.models import User
import datetime

class Forum(models.Model):
    topic_name = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    def __str__(self):
        return self.topic_name

class Thread(models.Model):
    thread_name = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.datetime.now())
    poster = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)
    def __str__(self):
        return self.thread_name

class Comment(models.Model):
    content = models.TextField(max_length=800)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    poster = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now())

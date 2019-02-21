from django.db import models
from django.contrib.auth.models import User

DEFAULT_TOPIC_ID = 1

class Topic(models.Model):
    name = models.CharField(max_length=30)

class Forum(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=120)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE, default=DEFAULT_TOPIC_ID)
    def __str__(self):
        return self.name

class Thread(models.Model):
    name = models.CharField(max_length=30)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)

class Post(models.Model):
    content = models.CharField(max_length=8000)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    poster = models.OneToOneField(User,on_delete=models.CASCADE)

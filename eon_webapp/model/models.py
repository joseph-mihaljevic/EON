from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

def content_file_name(instance, filename):
    return '/'.join(['content', instance.user.username, filename])

# Create your models here.
class UserModel(models.Model):
    model_name = models.CharField(max_length=30)
    #author_PK = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(User)
    created_by = models.CharField(max_length=256,default='User')
    folder_location = models.CharField(max_length=128)
    uploaded_code = models.FileField()
    #file = models.FileField(upload_to=content_file_name)
    description = models.CharField(max_length=256,default='Type Here...')
    #Temp - Remove this for forum PK
    #forum_pk = models.ForeignKey(User, on_delete='PROTECT')
    #user_pk = models.ForeignKey(0, on_delete='PROTECT')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    EONid = models.CharField(max_length=256)
    #Value.objects.annotate(as_float=Cast('integer', FloatField())).get()
    #EONid = "EON.M." + CharField(Created.month) + "." + CharField(Created.year) + "." + name

    def get_absolute_url(self):
        return reverse('Display-UserModel', kwargs={'pk':self.pk})
        #return reverse('model_index')
    #def Some_url(self):



    def __str__(self):
        return self.EONid

    def SaveGraphDiscriptions(self):
        print("Coming soon")

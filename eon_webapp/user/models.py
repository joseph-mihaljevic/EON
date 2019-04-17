from django.db import models
from django.contrib.auth.models import User
from forum.models import Forum
from django.urls import reverse
# Create your models here.
from model.models import UserModel
from forum.models import Thread, Forum, Comment
from django.contrib.auth.models import User




#class User_Likes_Models(models.Model):
#    user = models.ManyToManyField(User)
#    liked_models = models.ForeignKey(User, related_name='vu_f',null=True, on_delete="remove")


class Profile(models.Model):
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.TextField(max_length=500)
    bio = models.TextField(max_length=500, blank=True)
    email = models.TextField(max_length=500, blank=True)
    affiliation = models.TextField(max_length=500, blank=True)
    name = models.TextField(max_length=500, blank=True)
    def get_absolute_url(self):
        return reverse('dashboard')
        #return reverse('display_UserInfo', kwargs={'username':self.pk})
    @classmethod
    def make_profile(cls, user_pk):
        profile, created = cls.objects.get_or_create(
            user_pk = user_pk,
            email = 'No Email',
            name = 'No Name',
            pic = 'https://heapanalytics.com/wp-content/uploads/2013/12/interactive-line-graph.png',
            bio = 'No Biography',
            affiliation = 'No Affiliation'
        )

        profile.save()



class Friend(models.Model):
    user         = models.ForeignKey(User, related_name='u_f',null=True, on_delete="remove")
    viewing_user = models.ForeignKey(User, related_name='vu_f',null=True, on_delete="remove")

    @classmethod
    def make_friend(cls, viewing_user, user):
        friend, created = cls.objects.get_or_create(
            viewing_user=viewing_user,
            user=user
        )

        friend.save()

    @classmethod
    def lose_friend(cls, viewing_user,user):
        friend, created = cls.objects.get_or_create(
            viewing_user=viewing_user,
            user=user
        )
        friend.delete()
        friend.save()

class FriendRequest(models.Model):
    user         = models.ForeignKey(User, related_name='u_fr',null=True, on_delete="remove")
    viewing_user = models.ForeignKey(User, related_name='vu_fr',null=True, on_delete="remove")

    @classmethod
    def make_FriendRequest(cls, viewing_user, user):
        FriendRequest, created = cls.objects.get_or_create(
            viewing_user=viewing_user,
            user=user
        )

        FriendRequest.save()


    @classmethod
    def remove_FriendRequest(cls, viewing_user,user):
        FriendRequest, created = cls.objects.get_or_create(
            viewing_user = viewing_user,
            user=user
        )
        FriendRequest.delete()
        #FriendRequest.save()

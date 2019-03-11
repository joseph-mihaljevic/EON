from django.db import models
from django.contrib.auth.models import User
from forum.models import Forum
# Create your models here.
from model.models import UserModel




#class User_Likes_Models(models.Model):
#    user = models.ManyToManyField(User)
#    liked_models = models.ForeignKey(User, related_name='vu_f',null=True, on_delete="remove")






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
        FriendRequest.save()

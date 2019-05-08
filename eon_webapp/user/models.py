from django.db import models
from django.contrib.auth.models import User
from forum.models import Forum
from django.urls import reverse
# Create your models here.
from model.models import UserModel
from forum.models import Thread, Forum, Comment
from django.contrib.auth.models import User





# As the default User profile doesn't contain all the fields we need, we
# created a simple 1 to 1 table to store all of a user’s information.
class Profile(models.Model):
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.TextField(max_length=500)

    #The following are fextfields to store User profile personal information)
    bio = models.TextField(max_length=500, blank=True)
    email = models.TextField(max_length=500, blank=True)
    affiliation = models.TextField(max_length=500, blank=True)
    name = models.TextField(max_length=500, blank=True)

    #This is a Django function that allows redirects after editing or creating
    # Table entries
    def get_absolute_url(self):
        return reverse('dashboard')
        #return reverse('display_UserInfo', kwargs={'username':self.pk})

    #Is Ran when a user first visits their profile page. This function creates a Profile table for that given user.
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


#Is a Table representing Freindship relations between users.
# a Friend relation is created after a FriendRequest has been made,
# and is accepted
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

#Is a Table representing FriendRequests made between users. 
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

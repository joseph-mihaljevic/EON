from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Group(models.Model):
    group_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    #group_admin = models.ForeignKey(User,on_delete="nothing")
    about = models.CharField(max_length=100, blank=True, null=True)
    #group_forum = models.ForeignKey(Forum, on_delete="remove")
    #private = models.

    #@classmethod
    #def make_friend(cls, current_user, new_friend):
    #    friend, created = cls.objects.get_or_create(
    #        current_user=new_friend
    #    )
    #    print(friend.current_user.pk)
    #    friend.save()

    def __str__(self):
        return self.pk
    def get_absolute_url(self):
        #return reverse('model_index')
        return reverse('view-group', kwargs={'groupname':self.name})

    @classmethod
    def make_Group(cls, group_admin):
        group, created = cls.objects.get_or_create(
            group_admin=group_admin
        )

        group.save()


class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.user.username



class JoinGroupRequest(models.Model):
    invite_user  = models.ForeignKey(User, related_name='u_gr', on_delete=models.CASCADE)
    group_member = models.ForeignKey(User, related_name='fu_gr', on_delete=models.CASCADE)
    group        = models.ForeignKey(Group,on_delete=models.CASCADE)



#class GroupForum(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    group = models.ForeignKey(Group,on_delete=models.CASCADE)
#
#    def __str__(self):
#        return self.user.username

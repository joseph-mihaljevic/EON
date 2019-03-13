from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.




class Group(models.Model):
    #group_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=100, null=True)
    #group_forum = models.ForeignKey(Forum, on_delete="remove")
    #private = models.

    #@classmethod
    #def make_friend(cls, current_user, new_friend):
    #    friend, created = cls.objects.get_or_create(
    #        current_user=new_friend
    #    )
    #    print(friend.current_user.pk)
    #    friend.save()


    #def get_absolute_url(self):
        #return reverse('model_index')
    #    return reverse('view-group', kwargs={'groupname':self.name})
    @classmethod
    def make_group(cls, name,about,user):

        print("1",name,about)
        Group, created = cls.objects.get_or_create(
            name = name,
            about = about
        )
        print(Group.pk)
        Group.save()
        #GroupMember.addAdmin(Group = group, user = user)
        #GroupMember.addUser(Group = group, user = user)
        GroupMember.addAdmin(Group,user)
        #group.set()


class GroupMember(models.Model):
    user  = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group,null=True)
    admin = models.BooleanField(default=False)
    @classmethod
    def addAdmin(cls, group, user):
        admin = GroupMember(user=user,admin = True)
        admin.save()
        admin.group.add(group)
        admin.save()
    @classmethod
    def addUser(cls, group, user):
        groupMember, created = cls.objects.get_or_create(
            group=group,
            user=user
        )
        print("groupmem.pk")
        print(groupMember.pk)
        groupMember.save()

class JoinGroupRequest(models.Model):
    user  = models.ForeignKey(User, related_name='j_gr', on_delete=models.CASCADE)
    group        = models.ForeignKey(Group,on_delete=models.CASCADE)


class InviteGroupRequest(models.Model):
    invite_user  = models.ForeignKey(User, related_name='i_gr', on_delete=models.CASCADE)
    group_member = models.ForeignKey(User, related_name='fi_gr', on_delete=models.CASCADE)
    group        = models.ForeignKey(Group,on_delete=models.CASCADE)
    @classmethod
    def make_InviteGroupRequest(cls, viewing_user, user):
        FriendRequest, created = cls.objects.get_or_create(
            viewing_user=viewing_user,
            user=user
        )

        FriendRequest.save()
#class GroupForum(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    group = models.ForeignKey(Group,on_delete=models.CASCADE)
#
#    def __str__(self):
#        return self.user.username

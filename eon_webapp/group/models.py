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
    group = models.ManyToManyField(Group)
    admin = models.BooleanField(default=False)
    @classmethod
    def addAdmin(cls, group, user):
        Member = GroupMember(user=user,admin = True)
        Member.save()
        Member.group.add(group)
        Member.save()
    @classmethod
    def addUser(cls, group, user):
        Member = GroupMember(user=user,admin = False)
        Member.save()
        Member.group.add(group)
        Member.save()
    @classmethod
    def removeUser(group, user):
        Member, created = GroupMember.objects.get_or_create(
            group = group,
            user = user
        )
        Member.remove(group)
class JoinGroupRequest(models.Model):
    user         = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    group        = models.ManyToManyField(Group)
    @classmethod
    def make_InviteGroupRequest(cls, group, user):
        JoinGroupRequest, created = cls.objects.get_or_create(
            group=group,
            user=user
        )

        JoinGroupRequest.save()
    @classmethod
    def make_InviteGroupRequest_1(cls, group, user):
        #Join Group Request
        JGR = JoinGroupRequest(user=user)
        JGR.save()
        JGR.group.add(group)
        JGR.save()
    def remove_InviteGroupRequest_1(group, user):
        JGR, created = JoinGroupRequest.objects.get_or_create(
            group = group,
            user = user
        )
        JGR.delete()

class GroupInvite(models.Model):
    invite_user  = models.ForeignKey(User, related_name='i_gr', on_delete=models.CASCADE)
    group_member = models.ForeignKey(User, related_name='fi_gr', on_delete=models.CASCADE)
    group        = models.ManyToManyField(Group)
    @classmethod
    def make_InviteGroupRequest(cls, viewing_user, user):
        FriendRequest, created = cls.objects.get_or_create(
            viewing_user=viewing_user,
            user=user
        )

        FriendRequest.save()
    def make_GroupInvite( group, invite_user,group_member):
        #Join Group Request
        GI = GroupInvite(invite_user=invite_user,group_member=group_member)
        GI.save()
        GI.group.add(group)
        GI.save()
    def remove_GroupInvite(group, user):
        GI, created = JoinGroupRequest.objects.get_or_create(
            group = group,
            user = user
        )
        GI.delete()
#class GroupForum(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    group = models.ForeignKey(Group,on_delete=models.CASCADE)
#
#    def __str__(self):
#        return self.user.username

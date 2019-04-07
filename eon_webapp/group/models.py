from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

USER_PRIVILEGES_CHOICES = (
      (1, 'Admin'),
      (2, 'Moderator'),
      (3, 'Contributor'),
      (4, 'Member'),
  )



class Group(models.Model):
    #group_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=500, null=True)
    # These values denote the access of
    Private = models.BooleanField(default=False)
    Editable = models.BooleanField(default=False)
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
        #print("1",name,about)
        Group, created = cls.objects.get_or_create(
            name = name,
            about = about
        )
        #print(Group.pk)
        Group.save()
        #GroupMember.addAdmin(Group = group, user = user)
        #GroupMember.addUser(Group = group, user = user)
        GroupMember.addAdmin(Group,user)
        #group.set()
    @classmethod
    def changePrivacyPreference(cls, name, Private):
        print("calling get_or_create")
        Editing_Group = Group.objects.get(name = name)

        Editing_Group.Private = Private
        Editing_Group.save()
        return True

    def changeEditablePreference(cls, group, Editable):
        print("calling get_or_create")
        Editing_Group, created = cls.objects.get(name = name)
        Editing_Group.Editable = Editable
        Editing_Group.save()
        return True
    def get_absolute_url(self):
        #return reverse('model_index')
        return reverse('view-group', kwargs={'groupname':self.name})




class GroupMember(models.Model):
    user  = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group)
    admin = models.BooleanField(default=False)
    role  = models.PositiveSmallIntegerField(choices = USER_PRIVILEGES_CHOICES)
    @classmethod
    def Get_UserGroups(cls, userPK):
        User_GroupMember = GroupMember.objects.filter(user = userPK)

        UsersGroups = [Membership.group.all()[0] for Membership in User_GroupMember]
        return UsersGroups



    @classmethod
    def UserHas_Manage_Privlege(cls, userPK,group):
        GroupMembers = cls.objects.filter(
            group = group,
            user = userPK
        )

        if not GroupMembers.count():
            return False
        GroupMember = GroupMembers[0]

        if ((GroupMember.role == 1) | (GroupMember.role == 2)):
            return True
        return False
        #if (userPK.role):

    @classmethod
    def UserHas_Edit_Privlege(cls, userPK,group):
        print(group.Editable)
        if (group.Editable):
            return True
        #print(userPK)

        GroupMember = cls.objects.filter(
            group = group,
            user = userPK
        )
        if not GroupMember.count():
            return False
        GroupMember = GroupMember[0]
        if ((GroupMember.role == 1) | (GroupMember.role == 2) | (GroupMember.role == 3)):
            return True
        return False

    @classmethod
    def UserHas_View_Privlege(cls, userPK,group):
        if (not (group.Private)):
            return True
        GroupMember = cls.objects.filter(
            group = Group,
            user = userPK
        )
        if not GroupMember.count():
            return False
        GroupMember = GroupMember[0]
        if ((GroupMember.role == 1) | (GroupMember.role == 2) | (GroupMember.role == 3)):
            return True
        return False
    @classmethod
    def UserIsMember(cls, userPK,group):
        GroupMember = cls.objects.filter(
            group = group,
            user = userPK
        )
        if not GroupMember.count():
            return False
        return True
        #GroupMember.remove(group)
    @classmethod
    def changeRole(cls, userPK, group, role):
        print("calling get_or_create")
        GroupMember, created = cls.objects.get_or_create(
            group = group,
            user = userPK
        )
        GroupMember.role = role
        if (role ==1):
            GroupMember.admin = True
        else:
            GroupMember.admin = False
        print(" GroupMember.admin changing To : ",GroupMember.admin)
        GroupMember.save()
        return True
    #TODO change Parameter name user to userPK
    #TODO change Parameter group to Group
    @classmethod
    def addAdmin(cls, group, user):
        Member = GroupMember(user=user,admin = True,role=1)
        Member.save()
        Member.group.add(group)
        Member.save()
    @classmethod
    def addUser(cls, group, user,role=4):
        Member = GroupMember(user=user,admin = False,role=4)
        Member.save()
        Member.group.add(group)
        Member.save()
    @classmethod
    def removeUser(cls,group, user):
        GroupMember = cls.objects.get(
            group = group,
            user = user
        )
        GroupMember.delete()



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
    def JoinRequest_Made(cls, group, userPK):
        JoinGR= cls.objects.filter(
            group=group,
            user=userPK
        )
        if not JoinGR.count():
            return False
        return True

    @classmethod
    def make_InviteGroupRequest_1(cls, group, userPK):
        userObject = User.objects.get(pk=userPK)
        #Join Group Request
        JoinGR = JoinGroupRequest(user=userObject)
        JoinGR.save()
        JoinGR.group.add(group)
        JoinGR.save()
    def remove_InviteGroupRequest_1(group, userPK):
        JoinGR, created = JoinGroupRequest.objects.get_or_create(
            group = group,
            user = userPK
        )
        JoinGR.delete()

class GroupInvite(models.Model):
    invite_user  = models.ForeignKey(User, related_name='i_gr', on_delete=models.CASCADE)
    group_member = models.ForeignKey(User, related_name='fi_gr', on_delete=models.CASCADE)
    group        = models.ManyToManyField(Group)
    @classmethod
    def GroupInvite_Made(cls, group, invite_userPK):
        GI = cls.objects.filter(
            group = group,
            invite_user = invite_userPK
        )
        if not GI.count():
            return False
        return True

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

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Group,GroupMember,JoinGroupRequest,GroupInvite
from user.models import Friend
from .forms import GroupForm
from django.contrib.auth.models import User

# Create your views here.



def searchGroup_Form(request):
    return render(request, 'users/searchUsers_Form.html')

def searchGroup_Results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        users = group.objects.filter(username__icontains=q)
        return render(request, 'users/searchUsers_Results.html',
                      {'users': users, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')


def view_group(request,groupname):
    context = {}
    #print(groupname)
    context["Group"] =  Group.objects.filter(name = groupname)
    if not context["Group"]:
        return render(request, '404.html',{"Message": "Group Not Found!"})
    context["Group"] = context["Group"][0]
    #TODO Change Admin to Manage_Privlege variable use, makes life easier
    context["Manage_Privlege"] = GroupMember.UserHas_Manage_Privlege(userPK = request.user.pk, group = context["Group"])
    context["View_Privlege"] = GroupMember.UserHas_View_Privlege(userPK = request.user.pk, group = context["Group"])
    context["Edit_Privlege"] = GroupMember.UserHas_Edit_Privlege(userPK = request.user.pk, group = context["Group"])

    context["members"] = GroupMember.objects.filter(group = context["Group"].pk)
    if (request.user.is_authenticated):
        context["Friends"] = Friend.objects.filter(viewing_user = request.user.pk)
        context["Friends"] = [x for x in context["Friends"] if not GroupMember.UserIsMember(group = context["Group"],userPK=x.pk)]
        print("filtered friends;",context["Friends"])
        context["JoinGroupRequsts"] = JoinGroupRequest.objects.filter(group = context["Group"])
        context["Admin"] = True
        #print(context["JoinGroupRequsts"][0].user)
        if(context["members"].filter(user=request.user)):
            context['Viewer_Member'] = True
            #print(context['Viewer_Member'])

    if(context["Group"]):
        if (request.method =='SEARCH'):
            if 'q' in request.GET and request.GET['q']:
                context['users'] = User.objects.filter(username__icontains=q)
                context['query'] = request.GET['q']
            else:
                return render(request, 'group/DetailedGroup.html', context)
            return render(request, 'group/DetailedGroup.html', context)
        else:
            return render(request, 'group/DetailedGroup.html', context)

    else:
        return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Experienced error !"})
    #return render(request, 'users/DetailedUser.html')




class GroupIndex(generic.ListView):
    #UserModel.objects.get(author_PK=User.pk)
    model = Group
    template_name = "group/index.html"

    fields = ["name"]
    def get_queryset(self):
        return Group.objects.all()

def list_groups(request):
    context = {}
    context['GroupInvites'] = GroupInvite.objects.filter(invite_user = request.user)
    context['Groups'] =  Group.objects.all()
    #print(context['GroupInvites'] )
    #groupMember = GroupMember.objects.filter(user =request.user.pk).all()
    #print(groupMember[0].group)
    #group = User.objects.filter(pk =request.user.pk).groupmember_set.all()
    #print(group)
    #list_friends = Friend.objects.filter(user =request.user.pk)
    #print(list_friends)
    #print(list_friends.count())
    return render(request, "group/index.html", context)

def CreateGroup(request):

    #if !groupname:
    print(request.method)
    if (request.method == 'GET'):
        form = GroupForm()
        fields = ['name','about']
        return render(request, 'group/Group_Create.html', {"From": form, "field": fields})
    if (request.method == 'POST'):
        form = GroupForm(request.POST)
        context = request.POST.dict()
        print(context['name'])
        alreadyExists = Group.objects.filter(name = context['name'])
        print(alreadyExists.count())
        if (alreadyExists.count()):
            return render(request, 'friend/FormFill_FriendRequest.html', {"from": " Group already exists !"})
        if form.is_valid():
            Group.make_group(name=context['name'],about=context['about'],user= request.user)
            #Group.objects.create(name = context['name'], about = context['about'])
            return render(request, 'group/Group_CreatedRedirect.html', {"Message": "Group: "+ context['name']+" Created !", "group":context['name']})

        else:
            return render(request, '404.html',{"Message": "You just submitted an invalid Group Form !"})
            #return render(request, 'friend/FormFill_FriendRequest.html', {"from": "You just submitted an invalid Group Form !"})
    return render(request, '404.html',{"Message": "Experienced group doesnt exist!"})
    #model.created_by = request.user

    #context_object_name = ""


    #friends = Group.objects.filter(user=changing_friend.pk,viewing_user= request.user.pk).count()


    #context_object_name = "UserModel"

#def CreateGroup(request):
#    make_Group


def Manage_Recruits(request,groupname,operation,userPK):
    context = {}
    #print(groupname)
    context["Group"] = Group.objects.get(name = groupname)

    context["members"] = GroupMember.objects.filter(group=context["Group"].pk)
    if (request.user.is_authenticated):
        friend = Friend.objects.filter(viewing_user = request.user.pk)

        friend = [x for x in friend if GroupMember.UserIsMember(group = context["Group"],userPK=x.pk)]
        print("filtered friends;",friend)
        context["Friends"] = friend
        if(context["members"].filter(user=request.user)):
            context['Viewer_Member'] = True
            print(context['Viewer_Member'])

    if(context["Group"]):
        context["joingroupRequsts"] = JoinGroupRequest.objects.filter(group = context["Group"])
        print(context["joingroupRequsts"])

        if (operation =='search'):
            if 'q' in request.GET and request.GET['q']:
                q = request.GET['q']
                users = User.objects.filter(username__icontains=q)
                context['users'] = users
                context['query'] = q
            return render(request, 'group/DetailedGroup_InviteSearch.html', context)

        if (operation =='Apply'):
            if not JoinGroupRequest.JoinRequest_Made(group = context["Group"],userPK=request.user.pk):
                if not GroupInvite.GroupInvite_Made(group = context["Group"],invite_userPK=request.user.pk):
                    if not GroupMember.UserIsMember(group = context["Group"],userPK=request.user.pk):
                        JoinGroupRequest.make_InviteGroupRequest_1(group = context["Group"],userPK=request.user.pk)
                        context["Message"] = "Thanks for applying!"
                        return render(request, 'group/GroupMessage_Redirect.html',context)
                    else:
                        context["Message"] = "You are already a member"
                        return render(request, 'group/GroupMessage_Redirect.html',context)
                else:
                    GroupInvite.remove_GroupInvite(group = context["Group"],userPK=userPK)
                    GroupMember.addUser(group = context["Group"],user=newMember)
                    context["Message"] = "You have been added to the group"
                    return render(request, 'group/GroupMessage_Redirect.html',context)

                    #return render(request, '404.html',{"Message":  "You have been added to the group"})
            else:
                context["Message"] = "You have already applied to this group"
                return render(request, 'group/GroupMessage_Redirect.html',context)

            #check if application already exists


        if (operation == 'AcceptAppliedRequest'):
            context["Manage_Privlege"] = GroupMember.UserHas_Manage_Privlege(userPK = request.user.pk, group = context["Group"])
            context["View_Privlege"] = GroupMember.UserHas_View_Privlege(userPK = request.user.pk, group = context["Group"])
            context["Edit_Privlege"] = GroupMember.UserHas_Edit_Privlege(userPK = request.user.pk, group = context["Group"])

            if (context["Manage_Privlege"]):
                newMember = User.objects.get(pk=userPK)

                if(JoinGroupRequest.JoinRequest_Made(group = context["Group"],userPK=userPK)):
                    JoinGroupRequest.remove_InviteGroupRequest_1(group = context["Group"],userPK=userPK)
                    if(GroupInvite.GroupInvite_Made(group = context["Group"],invite_userPK=userPK)):
                        GroupInvite.remove_GroupInvite(group = context["Group"],userPK=userPK)
                    GroupMember.addUser(group = context["Group"],user=newMember)

                context["Message"] = "User has been added to the group"
                return render(request, 'group/DetailedGroup.html',context)
            context["Message"] = "You are not signed in with the privlege to add users!"
            return render(request, 'group/GroupMessage_Redirect.html',context)

        if(operation =='Invite'):
            newMember = User.objects.get(pk=userPK)
            if GroupMember.UserIsMember(group = context["Group"],userPK=request.user.pk):
                context["Message"] = "User Already in group!"
                return render(request, 'group/GroupMessage_Redirect.html',context)
            if(JoinGroupRequest.JoinRequest_Made(group = context["Group"],userPK=userPK)):
                JoinGroupRequest.remove_InviteGroupRequest_1(group = context["Group"],userPK=userPK)
                GroupMember.addUser(group = context["Group"],user=newMember)

                context["Message"] = "User has been added to the group"
                return render(request, 'group/GroupMessage_Redirect.html',context)

            GroupInvite.make_GroupInvite(group = context["Group"],invite_user=newMember,group_member=request.user)

            context["Message"] = "Your Invite has been sent"
            return render(request, 'group/GroupMessage_Redirect.html',context)

        if(operation == 'Remove'):
            Member = User.objects.get(pk=userPK)
            GroupMemberRelationship = GroupMember.objects.get(group = context["Group"],user=Member)
            GroupMemberRelationship.delete()
            #GroupMember.addUser(group = viewing_group,user=newMember)
            context["Message"] ="User has been removed from the the group: "+context["Group"]
            return render(request, 'group/GroupMessage_Redirect.html',context)

        if (operation =='add'):
            if():
                #user exists+ not in group
                #add user
                return render(request, 'group/DetailedGroup.html', context)
            #otherwise display error

            #TODO implement Message Dialog
            context["Message"] = "User added to group !"
            context["Message"] = "User already in group !"
            context["Message"] = "User doesnt exist !"
            return render(request, 'group/DetailedGroup.html', context)
        else:
            return render(request, 'group/DetailedGroup.html', context)
    return render(request, '404.html',{"Message": "Experienced group doesnt exist!"})
        #return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Experienced group doesnt exist!"})

def Manage_Members(request,groupname):
    context = {}
    #print(groupname)
    context["Group"] = Group.objects.get(name = groupname)
    context["Admin"] = GroupMember.UserHas_Manage_Privlege(userPK = request.user.pk,group = context["Group"])

    #print("if request ----")
    if (request.user.is_authenticated):
        context["Friends"] = Friend.objects.filter(viewing_user =request.user.pk)
    #print("Groups ----")
    #print(context["Group"].pk)
    if(context["Group"]):
        context["members"] = GroupMember.objects.filter(group=context["Group"].pk)
        #print(context["members"])
        #GroupMember.objects.filter(group=viewing_group.pk)
        return render(request, 'group/Manage_Members.html',context)
    return render(request, '404.html',{"Message": "Group Not Found!"})


def Manage_Privlege(request,groupname,operation,User_pk):
    context = {}
    #print(groupname)
    context["Group"] = Group.objects.get(name = groupname)
    #context["Admin"] = True
    context["Admin"] = GroupMember.UserHas_Manage_Privlege(userPK = request.user.pk,group = context["Group"])


    if(operation == "MakeAdmin"):
        context['ActionPreformed'] = False
        if (context["Admin"]):
            context['ActionPreformed'] = GroupMember.changeRole(userPK= User_pk, group= context["Group"],role=1)
        return render(request, 'group/Manage_Privlege.html',context)

    if(operation == "MakeModerator"):
        context['ActionPreformed'] = False
        if (context["Admin"]):
            context['ActionPreformed'] = GroupMember.changeRole(userPK= User_pk, group= context["Group"],role = 2)
        return render(request, 'group/Manage_Privlege.html',context)

    if(operation == "MakeMember"):
        context['ActionPreformed'] = False
        if (context["Admin"]):
            context['ActionPreformed'] = GroupMember.changeRole(userPK= User_pk, group= context["Group"],role = 3)
        return render(request, 'group/Manage_Privlege.html',context)

    if(operation == "RemoveMember"):
        context['ActionPreformed'] = False
        if (context["Admin"]):
            RemovingUser = User.objects.get(pk=User_pk)
            context['ActionPreformed'] = GroupMember.removeUser(user= RemovingUser, group= context["Group"])
        return render(request, 'group/Manage_Privlege.html',context)

    return render(request, '404.html',{"Message": "Something went wrong !"})




class GroupDelete(DeleteView):
    model = Group
    context_object_name = "Group" #use this in the template
    success_url = reverse_lazy('MyGroups')
    template_name = 'group/Group_confirm_delete.html'

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Group,GroupMember
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
    #print(groupname)
    viewing_group= Group.objects.get(name = groupname)
    friend = Friend.objects.filter(viewing_user =request.user.pk)
    members = GroupMember.objects.filter(group=viewing_group.pk)


    if(viewing_group):
        print(viewing_group.about)
        return render(request, 'group/DetailedGroup.html', {"Group": viewing_group,'Friends':friend,'members':members})

    else:
        return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Experienced error !"})
    #return render(request, 'users/DetailedUser.html')


def list_groups(request):
    #current_user = User.objects.get(pk =request.user.pk)
    print("Calling group objects")
    user_groups = Group.objects.all()
    print("returning  group objects")
    #list_friends = Friend.objects.filter(user = request.user.pk)
    #print(list_friends)
    #print(list_friends.count())
    if(user_groups.count()):
        return render(request, 'group/List_Groups.html', {"Groups": user_groups})
    return render(request, 'group/List_Groups.html', {"from": "coming soon !"})
    #if(list_friends.count()):
        #return render(request, 'friend/List_Friends.html', {"from": "coming soon !"})

    #return render(request, 'friend/FormFill_FriendRequest.html', {"from": "coming soon !"})

class GroupIndex(generic.ListView):
    #UserModel.objects.get(author_PK=User.pk)
    model = Group
    template_name = "group/index.html"

    fields = ["name"]
    def get_queryset(self):
        return Group.objects.all()

def list_groups(request):
    group = Group.objects.all()
    #groupMember = GroupMember.objects.filter(user =request.user.pk).all()
    #print(groupMember[0].group)
    #group = User.objects.filter(pk =request.user.pk).groupmember_set.all()
    #print(group)
    #list_friends = Friend.objects.filter(user =request.user.pk)
    #print(list_friends)
    #print(list_friends.count())
    return render(request, "group/index.html", {"Groups": group})

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
            return render(request, 'friend/FormFill_FriendRequest.html', {"from": "You just submitted a Group Form !"})

        else:
            return render(request, 'friend/FormFill_FriendRequest.html', {"from": "You just submitted an invalid Group Form !"})
    #model.created_by = request.user

    #context_object_name = ""


    #friends = Group.objects.filter(user=changing_friend.pk,viewing_user= request.user.pk).count()


    #context_object_name = "UserModel"

#def CreateGroup(request):
#    make_Group

def change_members(request):
    return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Coming soon!"})


class DetailedGroupModel(generic.DetailView):
    model = Group
    context_object_name = "Group" #use this in the template
    template_name = 'Group/Group_UserModel.html'
    def get_queryset(self):
        return Group.objects.all()

class UpdateGroupModel(UpdateView):
    context = {}
    #context["ModelViewForm"] = ModelViewForm()
    model = Group

    fields = ['group_name','description']
    template_name = 'Group/Update_Group.html'

class DeleteGroupModel(DeleteView):
    model = Group
    context_object_name = "Group" #use this in the template
    success_url = reverse_lazy('model_index')
    template_name = 'Group/Group_confirm_delete.html'

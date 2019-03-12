from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Group,GroupMember
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
    print(groupname)
    viewing_group= Group.objects.get(name = groupname)

    if(viewing_group):
        print(viewing_group.about)
        return render(request, 'group/DetailedGroup.html', {"Group": viewing_group})

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
    if(True):
        model = Group
        template_name = "group/index.html"

        fields = ["name"]
    def get_queryset(self):
        return Group.objects.all()



class CreateGroup(CreateView):
    model = Group
    #model.created_by = request.user
    fields = ['name','about']
    #context_object_name = ""
    template_name = 'group/Group_Create.html'

    #context_object_name = "UserModel"

#def CreateGroup(request):
#    make_Group


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

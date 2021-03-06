from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash

from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from group.models import Group
from django.contrib.auth.models import User
from .models import Friend,FriendRequest,Profile
from user.forms import ChangeUserNameForm
from django.contrib import messages
from group.models import Group,GroupMember,JoinGroupRequest,GroupInvite
#for my testing
from django.http import HttpResponse

from django.contrib.auth.forms import PasswordChangeForm,UserChangeForm

from .admin import UserCreationForm
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class Dashboard(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'dashboard.html'


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            #request.user.logout()
            #return redirect('dashboard')
            return view_user(request,user.username)
            #return redirect('change_UserPassword')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/Change_UserPassword.html', {
        'form': form
    })


def change_username(request):
    if request.method == 'POST':
        form = ChangeUserNameForm(request.POST)#request.user, request.POST
        if form.is_valid():
            newusername = form.data["UserName"]
            print("NewUsername.objects:")
            print(User.objects.filter(username=newusername))
            if User.objects.filter(username=newusername).exists():
                print("Taken")
                messages.error(request, 'This UserName has already been taken!')
                #raise messages.error(request,u'Username "%s" is not available.' % newusername)
                #messages.success(request, 'This UserName has already been taken!')

            else:
                print("Changing")
                user = User.objects.get(username = request.user)
                user.username = newusername
                user.save()
                request.user.username = newusername
                messages.success(request, 'Your UserName was successfully updated!')

                return view_user(request,user.username)

        else:
            print("invalid form?")
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangeUserNameForm()#instance=request.user

        print("else:")
        print(form)

    return render(request, 'users/Change_UserName.html', {
        'form': form
    })



def view_Dashboard(request):
    context = {}
    context['Friend'] = Friend.objects.filter(viewing_user =request.user.pk)
    context['FriendRequest'] = FriendRequest.objects.filter(viewing_user= request.user.pk)
    context['Groups'] = GroupMember.Get_UserGroups(request.user.pk)
    #messages.success(request, 'Dashboard still being worked on !')
    #return redirect('dashboard')
    #TODO add models
    #TODO ? add recent forms ?
    return render(request, 'dashboard.html', context)
    #return render(request, 'dashboard.html', {"from": "coming soon !"})



def searchUsers_Form(request):
    return render(request, 'users/searchUsers_Form.html')

def searchUsers_Results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        users = User.objects.filter(username__icontains=q)
        return render(request, 'users/searchUsers_Results.html',
                      {'users': users, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')


def view_user(request,username):
    context = {}
    context['User'] = User.objects.get(username=username)
    context['Prof'] = Profile.objects.filter(user_pk=context['User'])
    print(context['Prof'])
    #if(context['Prof'])
    if(context['Prof'].count() == 0):
        Profile.make_profile(user_pk=context['User'])
        context['Prof'] = Profile.objects.filter(user_pk=context['User'])[0]
    else:
        context['Prof'] = Profile.objects.filter(user_pk=context['User'])[0]
    print(context['Prof'])
    if(username == request.user.username):
        context['User_Prof'] = True
    if(User):
        #return render(request, 'friend/FormFill_FriendRequest.html', {"from": "you cannot friend yourself !"})
        return render(request, 'users/DetailedUser.html',context)
    return render(request, 'friend/FormFill_FriendRequest.html', {"from": "coming soon !"})

def home(request):
    if request.user.is_authenticated:
        return (view_user(request,request.user.username))



class UpdateProfile(UpdateView):
    context = {}
    #context["Profile"] =
    model = Profile

    fields = ['name','pic','email','bio','affiliation']
    template_name = 'users/Update_Profile.html'
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)

        obj = super(UpdateProfile, self).get_object(*args, **kwargs)
        data['User_Prof'] = True
        if not obj.user_pk == self.request.user:
            data['User_Prof'] = False

        return data




def change_friendship(request,operation,friends_pk):
    changing_friend = User.objects.get(pk=friends_pk)
    #print(changing_friend)
    if not request.user.is_authenticated:
        return render(request, '404.html',{"Message": "You cannot make a friend request you are currently not loged in!"})
        #return render(request, 'friend/FormFill_FriendRequest.html', {"from": "You are currently not loged in!"})
    if(request.user.pk == friends_pk):
        if operation =='reject':
            #Friend.make_friend(request.user,changing_friend)
            FriendRequest.remove_FriendRequest(request.user,changing_friend)

            return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Friend request has been rejected"})
        print("cannot friend yourself!")
        return render(request, 'friend/FormFill_FriendRequest.html', {"from": "you cannot friend yourself !"})

    if(changing_friend):
        if operation == 'add':
            #return render(request, 'friend/FormFill_FriendRequest.html', {"from": "coming soon !"})
            #if(request.user.pk):

            #if friend request already made
            #                        ~~~
            #friends = Friend.objects.get(user= request.user.pk,viewing_user=changing_friend.pk)
            friends = Friend.objects.filter(user=changing_friend.pk,viewing_user= request.user.pk).count()
            print("Friends?:",friends)
            #specific_friend = friends.objects.get(viewing_user=changing_friend.pk)
            if(friends):
                return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Already a friend!"})
            #~~~
            print("checking request")
            FriendRequest.make_FriendRequest(changing_friend,request.user)
            #Request_ForUser = FriendRequest.objects.filter(viewing_user=changing_friend.pk,user= request.user.pk).count()
            #print("checking request",Request_ForUser)
            #if(Request_ForUser):
            #    return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Already have sent a Friend request!"})
            #else:
            #    FriendRequest.make_FriendRequest(request.user,changing_friend)
            #    #render normal request submitted
            #    return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Friend request has been submitted"})
        elif operation =='accept':
            Friend.make_friend(request.user,changing_friend)
            Friend.make_friend(changing_friend,request.user)
            FriendRequest.remove_FriendRequest(changing_friend,request.user)
            return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Friend request has been accepted"})
        elif operation =='reject':
            #Friend.make_friend(request.user,changing_friend)
            FriendRequest.remove_FriendRequest(request.user,changing_friend)

            return render(request, 'friend/FormFill_FriendRequest.html', {"from": "Friend request has been rejected"})
        #elif operation == 'remove':
        #    friend.lose_friend(request.user,user,new_friend)
        return render(request, 'dashboard.html', {"forum_name": "nothing"})
    else:
        print("User does not exist! ")
        return render(request, 'dashboard.html', {"forum_name": "nothing"})


def list_friends(request):
    friend = Friend.objects.filter(viewing_user =request.user.pk)
    #print(friend)
    #list_friends = Friend.objects.filter(user =request.user.pk)
    #print(list_friends)
    #print(list_friends.count())
    return render(request, 'friend/List_Friends.html', {"Friend": friend})
    #if(list_friends.count()):
        #return render(request, 'friend/List_Friends.html', {"from": "coming soon !"})

    #return render(request, 'friend/FormFill_FriendRequest.html', {"from": "coming soon !"})



def list_FriendRequest(request):
    context = {}
    sent_request = FriendRequest.objects.filter(viewing_user= request.user.pk)
    if(sent_request.count()):
        context["Friend_Requests"] = sent_request
    return render(request, 'friend/List_FriendRequest.html', context)
    #return render(request, 'friend/List_FriendRequest.html', {"Friend": sent_request})

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from group.models import Group
from django.contrib.auth.models import User
from .models import Friend,FriendRequest,Profile

#for my testing
from django.http import HttpResponse

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class Dashboard(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'dashboard.html'


def view_Dashboard(request):
    friend = Friend.objects.filter(viewing_user =request.user.pk)
    sent_request = FriendRequest.objects.filter(viewing_user= request.user.pk)
    #TODO add models
    #TODO ? add recent forms ?
    return render(request, 'dashboard.html', {"Friend": friend,"sent_request": sent_request})
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


class UpdateProfile(UpdateView):
    context = {}
    #context["Profile"] =
    model = Profile

    fields = ['name','pic','email','bio','affiliation']
    template_name = 'users/Update_Profile.html'






def change_friendship(request,operation,friends_pk):
    changing_friend = User.objects.get(pk=friends_pk)
    print(changing_friend)
    print(changing_friend.pk)
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
    sent_request = FriendRequest.objects.filter(viewing_user= request.user.pk)
    if(sent_request.count()):
        return render(request, 'friend/List_FriendRequest.html', {"Friend": sent_request})
    return render(request, 'friend/FormFill_FriendRequest.html', {"from": "coming soon !"})

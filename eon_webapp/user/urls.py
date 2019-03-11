from django.urls import path
from . import views
from django.conf.urls import include, url


urlpatterns = [
    path('<slug:username>', views.view_user,name='user'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('dashboard/', views.Dashboard.as_view(),name='dashboard'),

    path(r'search/', views.searchUsers_Form,name='search_users'),
    path(r'search/Results/', views.searchUsers_Results),


    path(r'connect/<slug:operation>/<int:friends_pk>', views.change_friendship, name="change_friendship"),
    path(r'friends/', views.list_friends, name="friends"),
    path(r'friends/Requests/', views.list_FriendRequest, name="list_FriendRequest"),



]

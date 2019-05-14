from django.urls import path
from . import views
from django.conf.urls import include, url


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),

    path('<slug:username>', views.view_user,name='display_UserInfo'),
    path('home/', views.home,name='Home'),
    #path('edit/<int:pk>', views.UpdateProfile.as_view(),name='edit_UserInfo'),
    url(r'^edit/(?P<pk>\d+)/$', views.UpdateProfile.as_view(), name='edit_UserInfo'),
    url(r'^password/$', views.change_password, name='change_UserPassword'),
    url(r'^username/$', views.change_username, name='change_UserName'),
    path('dashboard/', views.view_Dashboard,name='dashboard'),

    path(r'search/', views.searchUsers_Form,name='search_users'),
    path(r'search/Results/', views.searchUsers_Results),


    path(r'connect/<slug:operation>/<int:friends_pk>', views.change_friendship, name="change_friendship"),
    path(r'friends/', views.list_friends, name="friends"),
    path(r'friends/Requests/', views.list_FriendRequest, name="list_FriendRequest"),



]

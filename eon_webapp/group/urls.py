from django.urls import path
from . import views
from django.conf.urls import include, url


urlpatterns = [
    path(r'Display/<slug:groupname>/', views.view_group,name='view-group'),
    #path(r'<int:pk>', views.view_group_byPK,name='view-group'),
    path('create/', views.CreateGroup.as_view(), name='create_group'),


    #path(r'search/', views.searchGroup_Form,name='search_group'),
    #path(r'search/Results/', views.searchGroup_Results),


    #path(r'connect/<slug:operation>/<int:friends_pk>', views.change_friendship, name="change_friendship"),
    path(r'MyGroups/', views.GroupIndex.as_view(), name="MyGroups"),
    #path(r'MyGroups/', views.list_groups, name="MyGroups"),

    #path(r'Groups/Requests/', views.list_FriendRequest, name="list_FriendRequest"),



]

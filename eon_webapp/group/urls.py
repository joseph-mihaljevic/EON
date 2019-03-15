from django.urls import path
from . import views
from django.conf.urls import include, url


urlpatterns = [
    path(r'Display/<slug:groupname>/', views.view_group,name='view-group'),
    #path(r'Display/<slug:groupname>/search', views.change_members, name="searchfor_members"),
    path(r'Display/<slug:groupname>/Member/<slug:operation>/<int:User_pk>', views.Manage_members, name="Manage_members"),
    #path(r'<int:pk>', views.view_group_byPK,name='view-group'),
    path('create/', views.CreateGroup, name='create_group'),
    path('delete/<int:pk>/', views.GroupDelete.as_view(), name='delete_group'),


    #path(r'search/', views.searchGroup_Form,name='search_group'),
    #path(r'search/Results/', views.searchGroup_Results),



    path(r'MyGroups/', views.list_groups, name="MyGroups"),
    #path(r'MyGroups/', views.list_groups, name="MyGroups"),

    #path(r'Groups/Requests/', views.list_FriendRequest, name="list_FriendRequest"),



]

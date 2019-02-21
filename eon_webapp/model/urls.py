from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('index/', views.Index.as_view(), name='model_index'),
    url(r'CreateUserModel/', views.CreateUserModel.as_view(),name='Create-UserModel'),

    #url('DetailedUserModel', views.DetailedUserModel.as_view(),name='Detailed-UserModel'),
    path(r'Display_UserModel/<int:pk>/', views.DetailedUserModel.as_view(),name='Display-UserModel'),
    #url(r'UpdateUserModel/', views.UpdateUserModel.as_view(),name='Update-UserModel'),
    path(r'UpdateUserModel/<int:pk>/', views.UpdateUserModel.as_view(),name='Update-UserModel'),
    #path('DeleteUserModel/<int:section>/', views.DeleteUserModel.as_view(),name='Delete-UserModel'),
]

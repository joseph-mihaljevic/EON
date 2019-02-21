from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.Index.as_view(), name='forum_index'),
    path('create/', views.CreateForum.as_view(), name='forum_create'),
    path('view/<in_id>', views.ViewForum, name='forum_view'),
]

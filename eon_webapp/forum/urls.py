from django.urls import path
from . import views

# Setting up required urlpatterns
urlpatterns = [
    path('index/', views.Index.as_view(), name='forum_index'),
    path('create/', views.CreateForum.as_view(), name='forum_create'),
    path('<forum_id>/create', views.CreatePost.as_view(), name='thread_create'),
    path('view/<in_id>', views.ViewForum, name='forum_view'),
    path('view/thread/<thread_id>', views.ViewThread, name='thread_view'),
    # path('view/thread/<thread_id>/comment', views.CreateComment.as_view(), name='comment_create'),
    # path('view/<thread_id>', views.CreatePost.as_view(), name='thread_create'),
]

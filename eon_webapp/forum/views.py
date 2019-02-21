from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Forum, Topic, Thread
from .forms import ForumCreationForm, PostCreationForm


class Index(generic.ListView):
    model = Forum
    template_name = 'forum/index.html'
    context_object_name = 'forums'
    def get_queryset(self):
        """Return all forums"""
        return Forum.objects.all()

class CreateForum(generic.CreateView):
    form_class = ForumCreationForm
    success_url = reverse_lazy('forum_index')
    template_name = 'forum/create_forum.html'

class CreatePost(generic.CreateView):
    form_class = PostCreationForm
    success_url = ('forum_index')
    template_name = 'forum/create_post.html'


def ViewForum(request,in_id):
    forum = Forum.objects.get(id=int(in_id))
    print(forum.name)
    threads = Thread(forum=forum)
    return render(request, 'forum/view.html', {"forum_name":forum.name,"forum_desc":forum.description})

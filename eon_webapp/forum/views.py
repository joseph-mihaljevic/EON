from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from .models import Forum, Thread, Comment
from .forms import ForumCreationForm, PostCreationForm, CommentCreationForm


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
    success_url = reverse_lazy('forum_index')
    template_name = 'forum/create_post.html'

    def form_valid(self, form):
        form.instance.forum = Forum.objects.get(id=self.kwargs['forum_id'])
        form.instance.poster = self.request.user
        return super(CreatePost, self).form_valid(form)

class CreateComment(generic.CreateView):
    form_class = CommentCreationForm
    model = Comment
    template_name = 'forum/create_comment.html'

    def form_valid(self, form):
        # form.instance.comment = Comment.objects.get(id=self.kwargs['thread_id'])
        form.instance.poster = self.request.user
        form.instance.thread = Thread.objects.get(id=self.kwargs['thread_id'])
        self.success_url = reverse_lazy('thread_view',kwargs={"thread_id": self.kwargs['thread_id']})

        return super(CreateComment, self).form_valid(form)

def ViewForum(request,in_id):
    forum = Forum.objects.get(id=int(in_id))
    threads = Thread.objects.filter(forum = forum)
    return render(request, 'forum/view.html', {"forum_id": forum.id, "forum_name":forum.topic_name,"forum_desc":forum.description,"threads":threads})

def ViewThread(request,thread_id):
    thread = Thread.objects.get(id=int(thread_id))
    comments = Comment.objects.filter(thread = thread)
    return render(request, 'forum/thread.html', {"thread":thread,"comments":comments})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from .models import Forum, Thread, Comment, Reply
from group.models import Group, GroupMember
from .forms import ForumCreationForm, PostCreationForm, CommentCreationForm, ReplyCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect


class Index(generic.ListView):
    model = Forum
    template_name = 'forum/index.html'
    context_object_name = 'forums'
    def get_queryset(self):
        """Return all forums"""
        return Forum.objects.all()

# Class based so use mixin
class CreateForum(LoginRequiredMixin,generic.CreateView):
    form_class = ForumCreationForm
    success_url = reverse_lazy('forum_index')
    template_name = 'forum/create_forum.html'

# Class based so use mixin
class CreatePost(LoginRequiredMixin,generic.CreateView):
    form_class = PostCreationForm
    # success_url = reverse_lazy('forum_index')
    template_name = 'forum/create_post.html'

    def form_valid(self, form):
        form.instance.forum = Forum.objects.get(id=self.kwargs['forum_id'])
        form.instance.poster = self.request.user
        return super(CreatePost, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum_view', kwargs={'in_id': self.kwargs['forum_id']})

# class CreateComment(generic.CreateView):
#     form_class = CommentCreationForm
#     model = Comment
#
#     # def get_object(self,**kwargs):
#     #     pk_ = self.kwargs.get("id")
#     #     return get_object_or_404(Thread,pk = pk_)
#     #
#     # def get_context_data(self, **kwargs):
#     #     thread = self.object
#     #     comments = Comment.objects.filter(thread = thread)
#     #     context ={ "thread":thread,"comments":comments }
#
#     def form_valid(self, form):
#         # form.instance.comment = Comment.objects.get(id=self.kwargs['thread_id'])
#         form.instance.poster = self.request.user
#         form.instance.thread = Thread.objects.get(id=self.kwargs['thread_id'])
#         self.success_url = reverse_lazy('thread_view',kwargs={"thread_id": self.kwargs['thread_id']})
#
#         return super(CreateComment, self).form_valid(form)

# Use get (request.user)
def ViewForum(request,in_id):
    forum = Forum.objects.get(id=int(in_id))
    threads = Thread.objects.filter(forum = forum)
    # get groupmember object
    groups = list()
    try:
        group_members = GroupMember.objects.filter(user = request.user)
        for group_member in group_members:
            for group in group_member.group.all():
                groups.append(group)
        print(groups)
        #     groups = None
    except ObjectDoesNotExist:
        group_member = None
        # grab all Groups
    print(groups)
    required_group = forum.group
    if (required_group is not None and required_group in groups) or (required_group is None):
        return render(request, 'forum/view.html', {"forum_id": forum.id, "forum_name":forum.topic_name,"forum_desc":forum.description,"threads":threads})
    else:
        return HttpResponseRedirect(reverse_lazy('forum_index'))

    # # see if user is in the group tied to the forum
    #
    # print(forum.group)
    # print(request.user)
    # print(grouper.pk)
    # # if request.user == grouper.pk:
    # # else:
    #     # you aren't part of this group

# Use decorators for permissions - no class based view
def ViewThread(request,thread_id):
    thread = Thread.objects.get(id=int(thread_id))

    if request.method == 'POST':
        print(request.POST)
        if request.POST and len(request.POST) > 0:
            form = None
            if request.POST['submit_type'] == "Comment":
                form = CommentCreationForm(request.POST)
            elif request.POST['submit_type'] == "Reply":
                form = ReplyCreationForm(request.POST)

            if form is not None:
                form.instance.poster = request.user
                form.instance.thread = Thread.objects.get(id=thread_id)

                if form.is_valid():
                    new_thing = form.save()

                    if isinstance(new_thing, Reply):
                        try:
                            parent_comment = Reply.objects.get(id=form.instance.parent_comment.pk)
                            new_entry = Reply(parent_comment=parent_comment)
                            if isinstance(new_thing, Comment):
                                new_entry.child_comment = new_thing
                            else:
                                new_entry.child_comment = new_thing.pk
                            print(new_entry, new_entry.child_comment, new_entry.parent_comment)
                            # new_entry.save()
                        except:
                            pass
                    return redirect("thread_view", thread_id=thread.id)
    else:
        form = CommentCreationForm()

    return render(request, 'forum/thread.html', {"form": form, "thread":thread})

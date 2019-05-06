# Required import statements
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

# Displays the forums available to the user but only the ones that they
# have access to
class Index(generic.ListView):
    model = Forum
    template_name = 'forum/index.html'
    context_object_name = 'forums'
    # Returns all the forums
    def get_queryset(self):
        forums = Forum.objects.all()
        forums = [forum for forum in forums if (forum.group==None or self.validate_user_in_forum_group(forum))]
        return forums
    # This function only displays the users groups he is on the forums
    def validate_user_in_forum_group(self,forum):
        if not self.request.user.is_authenticated:
            return False
        group_members = GroupMember.objects.filter(user=self.request.user)
        group_ids=[]
        # Creates all group_ids which the user is in
        for group_member in group_members:
            group_ids += [group.id for group in group_member.group.all()]
        if forum.group.id in group_ids:
            return True
        else:
            return False

# Creation of CreateForum class that verifies if they are signed in
# and displays a form to create a forum
class CreateForum(LoginRequiredMixin,generic.CreateView):
    form_class = ForumCreationForm
    success_url = reverse_lazy('forum_index')
    template_name = 'forum/create_forum.html'

# Creation of CreatePost class that verifies if they are signed in
# and displays a form to create a forum
class CreatePost(LoginRequiredMixin,generic.CreateView):
    form_class = PostCreationForm
    template_name = 'forum/create_post.html'

    # Returns essential information that can be used elsewhere
    def form_valid(self, form):
        form.instance.forum = Forum.objects.get(id=self.kwargs['forum_id'])
        form.instance.poster = self.request.user
        return super(CreatePost, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum_view', kwargs={'in_id': self.kwargs['forum_id']})


# Use get (request.user)
def ViewForum(request,in_id):
    forum = Forum.objects.get(id=int(in_id))
    threads = Thread.objects.filter(forum = forum)
    # get groupmember object
    groups = list()
    try:
        if not request.user.is_authenticated:
            group_member = None
        else:
            # Checking members of certain groups and adding them to a list
            group_members = GroupMember.objects.filter(user = request.user)
            for group_member in group_members:
                for group in group_member.group.all():
                    groups.append(group)
    except ObjectDoesNotExist:
        group_member = None
    # Grab all groups
    required_group = forum.group
    # Check if we can display the forum
    if (required_group is not None and required_group in groups) or (required_group is None):
        return render(request, 'forum/view.html', {"forum_id": forum.id, "forum_name":forum.topic_name,"forum_desc":forum.description,"threads":threads})
    else:
        return HttpResponseRedirect(reverse_lazy('forum_index'))

# Function that creates the structure of how a user will view a thread of comments in a forum
def ViewThread(request,thread_id):
    thread = Thread.objects.get(id=int(thread_id))

    if request.user.is_authenticated and request.method == 'POST':
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
                        except:
                            pass
                    return redirect("thread_view", thread_id=thread.id)
    else:
        form = CommentCreationForm()

    return render(request, 'forum/thread_container.html', {"form": form, "thread":thread, "view_source":"Forum"})

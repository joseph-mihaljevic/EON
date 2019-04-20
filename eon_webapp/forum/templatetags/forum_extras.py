from django import template
from ..forms import ReplyCreationForm
from ..models import Comment, Reply

register = template.Library()

@register.inclusion_tag("forum/_show_comments.html", takes_context=True)
def show_comments(context, thread):
    all_comments = list()
    comments = Comment.objects.filter(reply = None, thread_id = thread.id)

    for comment in comments:
        form = ReplyCreationForm()
        comment_replies = get_replies(comment)
        all_comments.append({
            "attributes": comment,
            "replies": comment_replies,
            "form": form})
    context['comments'] = all_comments
    return context

def get_replies(comment):
    all_replies = list();
    replies = Reply.objects.filter(parent_comment = comment)
    if len(replies) > 0:
        for reply in replies:
            form = ReplyCreationForm()
            all_replies.append({
                "attributes": reply,
                "form": form})
        return all_replies
    else:
        return list("")

@register.inclusion_tag("forum/_show_replies.html", takes_context=True)
def show_replies(context, reply):
    all_replies = list()
    gen_form = ReplyCreationForm(reply)
    replies = Reply.objects.filter(parent_comment = reply)

    for sub_reply in replies:
        form = ReplyCreationForm()
        sub_replies = get_replies(sub_reply)
        all_replies.append({"attributes": sub_reply,
                    "replies": sub_replies,
                    "form" : form})
    context['reply'] = reply
    context['form'] = gen_form
    context['replies'] = all_replies
    return context

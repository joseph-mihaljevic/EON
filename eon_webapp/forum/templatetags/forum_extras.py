from django import template
from ..forms import ReplyCreationForm
from ..models import Comment, Reply

register = template.Library()

@register.inclusion_tag("forum/_show_comments.html")
def show_comments(thread):
    all_comments = list()
    comments = Comment.objects.filter(reply = None, thread_id = thread.id)

    for comment in comments:
        form = ReplyCreationForm()
        comment_replies = get_replies(comment)
        all_comments.append({
            "attributes": comment,
            "replies": comment_replies,
            "form": form})
    return {'comments': all_comments}

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

@register.inclusion_tag("forum/_show_replies.html")
def show_replies(reply):
    all_replies = list()
    gen_form = ReplyCreationForm(reply)
    replies = Reply.objects.filter(parent_comment = reply)

    for sub_reply in replies:
        form = ReplyCreationForm()
        sub_replies = get_replies(sub_reply)
        all_replies.append({"attributes": sub_reply,
                    "replies": sub_replies,
                    "form" : form})
    return {'reply': reply, 'form': gen_form, 'replies': all_replies}

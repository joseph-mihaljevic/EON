from django.contrib import admin
from .models import Forum,Thread,Comment,Reply

# Make sure to register models here

class ForumAdmin(admin.ModelAdmin):
    list_display = ('topic_name','description')

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('thread_name','forum')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content','thread','poster')

admin.site.register(Comment,CommentAdmin)
admin.site.register(Thread,ThreadAdmin)
admin.site.register(Forum,ForumAdmin)
admin.site.register(Reply)

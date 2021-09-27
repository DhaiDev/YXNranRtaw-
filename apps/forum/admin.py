from django.contrib import admin

# Register your models here.
from apps.forum.models import Semester, Subject, Topic, Comment

admin.site.register(Semester)
admin.site.register(Subject)


# admin.site.register(Comment)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

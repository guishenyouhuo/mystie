from django.contrib import admin
from .models import LikeCount, LikeRecord


# Register your models here.


@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'content_object', 'liked_num')


@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'content_object', 'user', 'liked_time')

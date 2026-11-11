from django.contrib import admin
from notes.models import Notes, Tags, LikedNotes

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'user', 'count_likes', 'created_at')
    list_filter = ('created_at',)

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(LikedNotes)
class LikedNotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'user', 'liked_at')
    list_filter = ('liked_at',)
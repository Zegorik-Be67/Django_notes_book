from django.contrib import admin
from notes.models import Notes, Tags

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'user', 'created_at')
    list_filter = ('created_at',)

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tags')
from rest_framework import serializers
from notes.models import Notes

class NotesSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Notes
        fields = ['id', 'note', 'user', 'user_name', 'count_likes', 'created_at']
        read_only_fields = ['user', 'user_name', 'count_likes', 'created_at']
        ordering = ['created_at']

class NoteSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Notes
        fields = ['id', 'note', 'user', 'user_name', 'created_at']
        read_only_fields = ['user', 'user_name', 'created_at']
        ordering = ['-created_at']
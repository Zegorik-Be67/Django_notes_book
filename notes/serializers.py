from rest_framework import serializers
from notes.models import Notes, Tags, FavoriteNotes, LikedNotes, Comments

class NotesPublicSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Notes
        fields = ['id', 'user', 'user_name', 'note', 'created_at', 'likes_count']
        read_only_fields = ['id', 'user', 'user_name', 'created_at']
        ordering = ['created_at',]

    def get_likes_count(self, obj):
        return getattr(obj, 'liked_notes', 0)

class NotesPrivateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
        required=False,
        allow_null=True
    )
    class Meta:
        model = Notes
        fields = ['id', 'user', 'user_name', 'note', 'tags', 'created_at']
        read_only_fields = ['id', 'user', 'user_name', 'created_at']

class FavoriteNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteNotes
        fields = ['id', 'user', 'note', 'favorite_at']
        read_only_fields = ['id', 'user', 'favorite_at']

class LikedNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedNotes
        fields = ['id', 'user', 'note', 'liked_at']
        read_only_fields = ['id', 'user', 'liked_at']

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comments
        fields = ['id', 'user', 'user_name', 'note', 'comment', 'comment_at']
        read_only_fields = ['id', 'user', 'user_name', 'note', 'comment_at']
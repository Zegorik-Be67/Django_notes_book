from django.db import models
from django.contrib.auth.models import User

class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, blank=True, related_name='notes')
    note = models.TextField()
    count_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.id}: {self.note} - {self.count_likes}, {self.created_at}'

class LikedNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name='liked_notes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'note'],
                name='unique_liked_note',
            )
        ]

    def __str__(self):
        return f'{self.user.username}: {self.note} - {self.liked_at}'

class FavoriteNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name='favorite_notes')
    favorite_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'note'],
                name='unique_favorite_note',
            )
        ]

    def __str__(self):
        return f'{self.user.username}: {self.note} - {self.favorite_at}'

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Notes, on_delete=models.CASCADE, limit_choices_to={'is_private': False})
    comment = models.TextField()
    comment_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.note} - {self.comment_at}'
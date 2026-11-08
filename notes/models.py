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
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id}: {self.note} - {self.created_at}'

class LikedNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'note'],
                name='unique_liked_note',
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.note} - {self.liked_at}'
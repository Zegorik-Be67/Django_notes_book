from django.db import models
from django.contrib.auth.models import User

class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ManyToManyField(Tags, blank=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.note} - {self.created_at}'
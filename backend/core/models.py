from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    follow = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followed_by')

    def __str__(self):
        return self.username
    
class Post(models.Model):
    creater = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posts")
    caption = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.caption
    
class Media(models.Model):
    post = models.ForeignKey('Post', related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
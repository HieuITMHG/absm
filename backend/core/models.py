from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    follow = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followed_by')
    avatar = models.ForeignKey('Media', default= 44, blank=True, null=True, on_delete=models.CASCADE, related_name='post_avatar')
    def __str__(self):
        return self.username
    
class Post(models.Model):
    creater = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posts")
    caption = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.caption
    
class Media(models.Model):
    post = models.ForeignKey('Post', related_name='media', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='media/')

    def __str__(self):
        return f"{self.id} : {self.file.url}"
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
  user = models.ForeignKey(User, related_name='post', on_delete=models.DO_NOTHING)
  content = models.CharField(max_length=140, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  liked = models.ManyToManyField(User, related_name="like", blank=True, symmetrical=False )

  def __str__(self) -> str:
    return f"{self.content[:10]} by {self.user.username} @ {self.created_at: %H:%M,%Y-%m-%d}"
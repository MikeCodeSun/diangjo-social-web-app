from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
  name = models.CharField(max_length=10)
  follows = models.ManyToManyField('self', related_name="followed_by", symmetrical=False, blank=True)
  # 4.13 image upload 
  image = models.ImageField(upload_to='img/', blank=True)

  def __str__(self)  :
    return self.user.username

  def save(self, *args, **kwargs):
    if not self.name or self.name is None:
      print(self.name)
      self.name = self.user.username
    return super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
  if created:
    new_profile = Profile(user = instance)
    new_profile.save()
    new_profile.follows.add(instance.profile)
    new_profile.save()
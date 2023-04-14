from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User,Group
from .models import Profile
# Register your models here.
class ProfileInline(admin.StackedInline):
  model = Profile

class UserAdmin(ModelAdmin):
  model = User
  fields = ['username', 'password']
  inlines = [ProfileInline]

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

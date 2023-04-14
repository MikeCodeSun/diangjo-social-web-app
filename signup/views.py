from .form import LoginForm, SignupForm, NameForm, ImageForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.apps import apps
import os
from pathlib import Path
from django.contrib.auth.models import User

Post = apps.get_model('post', 'Post')

def login(r):
  if r.user.is_authenticated: 
    return redirect('post:index')
  form = LoginForm(r.POST or None)
  if r.method == "POST":
    if form.is_valid():
      user = form.cleaned_data.get('user')
      auth_login(r,user)
      return redirect('post:index')
    
  return render(r, 'registration/login.html', {'form': form})

def signup(r):
  if r.user.is_authenticated: 
    return redirect('post:index')
  form = SignupForm(r.POST or None)
  # print(r.POST)
  if r.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('signup:login')
    print(form)
  return render(r, 'registration/signup.html', {'form': form})

@login_required
def profile_list(r):
  profile_list = Profile.objects.exclude(user = r.user)

  return render(r, 'post/profile_list.html', {'profile_list': profile_list})
@login_required
def profile(r,pk):

  profile = Profile.objects.get(pk=pk)
  user_profile = r.user.profile

  if r.method == 'POST' and ('follow' in r.POST or 'unfollow' in r.POST):
    data = r.POST
    action = data.get('follow')
    if action == 'follow':
      user_profile.follows.add(profile)
    else:
      user_profile.follows.remove(profile)
    user_profile.save()
    return redirect('signup:profile', pk=pk)
  if r.method == 'POST' and 'delete' in r.POST:
    post_id = r.POST.get('delete')
    Post.objects.get(pk=post_id).delete()
    return redirect('signup:profile', pk=pk)
  if r.method == 'POST' and 'changename' in r.POST and r.user == profile.user :
    nameForm = NameForm(r.POST)
    if nameForm.is_valid():  
      name = nameForm.cleaned_data.get('name')
      user_profile.name = name
      user_profile.save()
    return redirect('signup:profile', pk=pk)
  if r.method == 'POST' and 'upload' in r.POST and r.user == profile.user:
    imgForm = ImageForm(r.POST, r.FILES)
    if not r.FILES :
      return render(r, 'post/profile.html', {'profile': profile})
    if imgForm.is_valid():
      if profile.image and profile.image is not None and profile.image.url :
        img_path =str(Path(__file__).parent.parent) + profile.image.url
        os.remove(img_path)
      profile.image = imgForm.cleaned_data.get('image')
      profile.save()
    return redirect('signup:profile', pk=pk)
  return render(r, 'post/profile.html', {'profile': profile})

def search_result(r):
  search_users = None
  if r.method == 'POST' and 'search' in r.POST:
    username = r.POST.get('username')
    search_users = User.objects.filter(
      username__icontains = username
    )
  return render(r, 'post/search_result.html',{'search_users': search_users} )
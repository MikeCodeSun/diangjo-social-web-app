from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .form import PostForm

# Create your views here.

@login_required
def index(r):
  posts = Post.objects.filter(
    user__profile__in = r.user.profile.follows.all()
  ).order_by("-created_at")
  form = PostForm(r.POST or None)
  # send new post
  if r.method == "POST" and 'newpost' in r.POST:
    new_post = form.save(commit=False)
    new_post.user = r.user
    new_post.save()
    return redirect('post:index')
    # like post logic 
  if r.method == "POST" and 'like' in r.POST:
    post_id = r.POST.get('like')
    
    like_post =Post.objects.get(pk = post_id)
    
    if r.user not in like_post.liked.all():
      
      like_post.liked.add(r.user)
    else:
      
      like_post.liked.remove(r.user)
    like_post.save()
    return redirect('post:index')
  return render(r, 'post/index.html', {'posts': posts, "form": form})
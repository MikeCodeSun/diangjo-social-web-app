from django.forms import ModelForm, CharField,Textarea
from .models import Post

class PostForm(ModelForm):
  content = CharField(max_length=140,required=True, widget=Textarea({'class': 'textarea', "placeholder": "最近的新鲜事..."}), label="")

  class Meta:
    model = Post
    exclude = ['user', 'liked']

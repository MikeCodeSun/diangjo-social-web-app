from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.forms import CharField,PasswordInput,TextInput, ImageField, FileInput
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from .models import Profile

class LoginForm(forms.Form):
  def __init__(self,  *args , **kwargs ) :
    super().__init__(*args, **kwargs)

  username = UsernameField(required=True,error_messages={"required": "必须填写用户名"}, widget=TextInput)

  password = CharField(widget=PasswordInput, error_messages={"required": "必须填写密码"})

  def clean(self):
    
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')

    if username and password:
      duplicate_name = User.objects.filter(username = username)
      if not duplicate_name.exists():
        self.add_error('username', "用户不存在")
        return username
      user = authenticate(username=username, password=password)
      print(f"clean: {user}")
      if user is  None:
        self.add_error('password', "密码错误")
        return password
      else:
        self.cleaned_data['user'] = user
        
    return self.cleaned_data

class SignupForm(UserCreationForm):
  username = UsernameField(
    required=True,
    max_length=20,
    min_length=3,
    error_messages={'required': "必须填写用户名", 'max_length': '用户名应该少于20个字母', 'unique': '用户名已经被注册','min_length': '用户名必须多于3个字母'},
    widget=TextInput,
    )
  password1 = CharField(
    required=True,
    min_length=8,
    error_messages={'required': "必须填写密码", 'min_length': '密码必须多于8个字母' ,'password_common':"密码"},
    widget=PasswordInput
  )
  password2 = CharField(
    required=True,
    min_length=8,
    error_messages={'required': "必须填写确认密码",'min_length': '确认密码必须多于8个字母','password_common':"密码" },
    widget=PasswordInput
  )
  error_messages = {'password_mismatch': '密码与确认密码不一致', 'password_common':"密码"}

class NameForm(forms.Form):
  name = CharField(label='',widget=TextInput)

class ImageForm(forms.ModelForm):
  
  class Meta:
    model = Profile
    fields = ['image']

  # def clean(self):
  #   cd = self.cleaned_data
  #   username = cd.get('username')
  #   password1 = cd.get('password1')
  #   password2 = cd.get('password2')

  #   if username and password1 and password2:
  #     duplicate_name = User.objects.filter(username = username)
  #     if duplicate_name.exists():
  #       self.add_error('用户名', '用户名已经被注册')
  #       return username
  #     if password1 != password2 :
  #       self.add_error('确认密码', '密码与确认密码不一致')
  #       return cd
      
  #     return super().clean()

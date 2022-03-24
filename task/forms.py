from django import forms
from django.contrib.auth.models import User

from task.models import UserProfile, Task


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserModifyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', 'phone_number')


class TaskForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Task
        fields = ('task_title', 'task_description', 'task_reward')

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_image', blank=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    tasks_posted = models.IntegerField(default=0)
    tasks_received = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    publisher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="publish")
    receiver = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="recieve", null=True)

    task_title = models.CharField(max_length=30)
    completion_state = models.BooleanField(default=0)
    task_description = models.TextField()
    task_reward = models.IntegerField(default=0)
    release_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_title

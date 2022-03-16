from django.contrib import admin
from task.models import UserProfile, Task
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'tasks_received', 'tasks_completed', 'tasks_posted')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'publisher', 'receiver', 'task_title', 'task_description', 'completion_state', 'task_reward', 'release_time')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Task, TaskAdmin)
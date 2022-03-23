from django.urls import path
from task import views
from django.conf.urls import url

app_name = 'task'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('taskpage/', views.taskpage, name='taskpage'),
    path('taskpage/taskpageid/', views.taskpageid, name='taskpageid'),
    path('usercenter/', views.usercenter, name='usercenter'),
    path('usercenter/posttask/', views.posttask, name='posttask'),
    path('usercenter/accepttask/', views.accepttask, name='accepttask'),
    path('usercenter/modifytheinformation/', views.modifytheinformation, name='modifytheinformation'),
    path('usercenter/changepassword/', views.changepassword, name='changepassword'),

    # User auth
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # For tests. Do not remove unless deployment.
    path('login-test/', views.test_login, name='login-test')
]
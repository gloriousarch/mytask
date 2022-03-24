from django.urls import path
from task import views
from django.conf.urls import url


app_name = 'task'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('taskpage/', views.taskpage, name='taskpage'),
    path('taskpage/taskpageid/', views.taskpageid, name='taskpageid'),
    path('taskpage/<slug:task_title_slug>/', views.show_task, name='show_task'),
    path('usercenter/', views.usercenter, name='usercenter'),
    path('usercenter/posttask/', views.posttask, name='posttask'),
    path('usercenter/list/', views.list, name='list'),
    path('usercenter/accepttask/', views.accepttask, name='accepttask'),
    path('usercenter/modifytheinformation/', views.modifytheinformation, name='modifytheinformation'),
    path('usercenter/changepassword/', views.changepassword, name='changepassword'),
    path('search_task/', views.search_task, name ='search_task'),


    #buttons
    path('task/<int:pk>/complete', views.CompleteTaskView.as_view(), name='complete-task'),
    path('task/<int:pk>/accepted', views.AcceptTaskView.as_view(), name='accept-task'),


    # User auth
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # For tests. Do not remove unless deployment.
    path('login-test/', views.test_login, name='login-test'),

    #ajax
 
]
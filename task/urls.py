from django.urls import path
from task import views
from django.conf.urls import url

app_name = 'task'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('login-test/', views.test_login, name='login-test'),
    path('logout/', views.user_logout, name='logout')
]
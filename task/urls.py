from django.urls import path
from task import views
from django.conf.urls import url

app_name = 'task'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

]
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from task.forms import UserForm
from task.models import UserProfile


def index(request):
    return render(request, 'task/index.html', )

def admin(request):
    return render(request, 'task/index.html', )

def about(request):
    return render(request, 'task/about.html', )

def register(request):
    return render(request, 'task/register.html', )




def user_register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = UserProfile(user=user)
            profile.save()

            return redirect(reverse('task:login'))
        else:
            return HttpResponseBadRequest(str(user_form.errors))
    else:
        user_form = UserForm()

    return HttpResponse('Register Page ¯\\_(ツ)_/¯ ')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('task:index'))
        else:
            return HttpResponse('Invalid username/password pair.')
    else:
        return HttpResponse('Login Page 👍')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('task:index'))


def test_login(request):
    if request.user.is_authenticated:
        return HttpResponse('Congrats, you are logged in!')
    else:
        return HttpResponseForbidden('Gotta login bruv')

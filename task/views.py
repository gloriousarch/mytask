import sys

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from task.forms import UserForm, UserProfileForm, UserModifyForm
from task.models import UserProfile


def index(request):
    return render(request, 'task/index.html', )


@login_required
def admin(request):
    return render(request, 'task/index.html', )


def about(request):
    return render(request, 'task/about.html', )


@login_required
def taskpage(request):
    return render(request, 'task/taskpage.html', )


@login_required
def taskpageid(request):
    return render(request, 'task/taskpageid.html', )


@login_required
def usercenter(request):
    return render(request, 'task/Usercenter.html', )


@login_required
def posttask(request):
    return render(request, 'task/posttask.html', )


@login_required
def accepttask(request):
    return render(request, 'task/accepttask.html', )


@login_required
def modifytheinformation(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserModifyForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if profile_form.is_valid() and user_form.is_valid():
            # Get user fields
            user_form.save()

            # Get profile fields
            if 'picture' in request.FILES:
                profile.picture = request.FILES['pictures']

            profile.save()
        else:
            print(profile_form.errors, user_form.errors)
    else:
        user_form = UserModifyForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    data = dict(
        profile_form=profile_form,
        user_form=user_form
    )
    return render(request, 'task/Usercenter.html', context=data)


@login_required
def changepassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        try:
            request.user.set_password(password)
            request.user.save()
        except Exception as e:
            _, _, tb = sys.exc_info()
            return HttpResponseServerError('Server Error: ' + tb)
    return render(request, 'task/Usercenter.html', )


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

    return render(request, 'task/register.html', )


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
            print(username, password)
            return HttpResponse('Invalid username/password pair.')
    else:
        return render(request, 'task/Login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('task:index'))


def test_login(request):
    if request.user.is_authenticated:
        return HttpResponse('Congrats, you are logged in!')
    else:
        return HttpResponseForbidden('Gotta login bruv')

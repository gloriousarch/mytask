import sys

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.shortcuts import reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from task.forms import UserForm, UserProfileForm, UserModifyForm, TaskForm
from task.models import UserProfile, Task
from django.core.paginator import Paginator

from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy


class CompleteTaskView(View):

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Task, pk=self.kwargs['pk'])

        obj.completion_state = not obj.completion_state
        obj.save()
        slug = obj.slug
        return redirect('/taskpage/'+slug)

def index(request):
    return render(request, 'task/index.html', )


@login_required
def admin(request):
    return render(request, 'task/index.html', )


def about(request):
    return render(request, 'task/about.html', )


@login_required
def taskpage(request):

    p = Paginator(Task.objects.order_by('-release_time').filter(completion_state=False, receiver=None), 3)
    page = request.GET.get('page')
    tasks = p.get_page(page)

    context_dict = {}
    context_dict['Tasks'] = tasks
    return render(request, 'task/taskpage.html', context=context_dict)


@login_required
def taskpageid(request):
    return render(request, 'task/taskpageid.html', )


@login_required
def usercenter(request):
    context_dict = {}
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Correct the database to make sure user has an associated profile
        userprofile = UserProfile(user=request.user)

    context_dict['userprofile'] = userprofile

    return render(request, 'task/Usercenter.html', context=context_dict)


@login_required
def posttask(request):
    posted = False

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.publisher = UserProfile.objects.get(user=request.user)
            task.save()

            posted = True
        else:
            print(form.errors)
    else:
        form = TaskForm()

    return render(request, 'task/posttask.html', context=dict(form=form, posted=posted))

@login_required
def list(request):

    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Correct the database to make sure user has an associated profile
        userprofile = UserProfile(user=request.user)

    print(userprofile.user)
    up = userprofile.user
    p = Paginator(Task.objects.order_by('-release_time').filter(receiver__user=up), 3)
    page = request.GET.get('page')
    tasks = p.get_page(page)

    context_dict = {}
    context_dict['Tasks'] = tasks
    return render(request, 'task/list.html', context=context_dict)


@login_required
def accepttask(request):
    task_accepted = False

    if request.method == 'POST':
        # A task ID is expected with the request.
        if 'task_id' not in request.POST:
            return HttpResponseBadRequest('\"task_id\" is a required field.')

        # Make sure the requested task exists
        try:
            task = Task.objects.get(task_id=request.POST['task_id'])
        except Task.DoesNotExist:
            return HttpResponseBadRequest('Task does not exist.')

        # Check and make sure task wasn't accepted by anyone else
        if task.receiver is not None:
            return HttpResponseBadRequest('Task was accepted by someone else.')

        # Get the profile associated with user
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)

        # Assign the task
        task.receiver = profile
        task.save()
        task_accepted = True

    p = Paginator(Task.objects.order_by('-release_time').filter(completion_state=False, receiver=None), 3)
    page = request.GET.get('page')
    tasks = p.get_page(page)

    context_dict = {}
    context_dict['Tasks'] = tasks

    return render(request, 'task/accepttask.html', context=dict(task_accepted=task_accepted, Tasks=tasks))


@login_required
def modifytheinformation(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Correct the database to make sure user has an associated profile
        profile = UserProfile(user=request.user)

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


##########################################################--db pages--##########################################################

def show_task(request, task_title_slug):
    context_dict = {}

    try:
        task = Task.objects.get(slug=task_title_slug)
        publisher = task.publisher
        userprofile = UserProfile.objects.get(user=publisher.user)
        context_dict['task'] = task
        context_dict['userprofile'] = userprofile


    except Task.DoesNotExist:
        context_dict['task'] = None
        context_dict['userprofile'] = None
        print("no")

    return render(request, 'task/taskpageid.html', context=context_dict)


def search_task(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        tasks = Task.objects.filter(task_title__contains=searched).filter(completion_state=False, receiver=None)
        return render(request, 'task/search_task.html', {'searched': searched, 'tasks': tasks})
    else:
        return render(request, 'task/search_task.html', )

##########################################################--ajax--##########################################################


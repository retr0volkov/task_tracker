from django.http import HttpResponse
from .models import Task, Worker, Stage
from django.shortcuts import get_list_or_404, render, get_object_or_404, redirect
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class TaskListView(LoginRequiredMixin, generic.ListView):
    login_url = '/tasks/login/'
    template_name = 'tracker/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        if (self.request.user.is_staff):
            return get_list_or_404(Task)
        else:
            tasks = Task.objects.filter(receiver=self.request.user)
            if tasks:
                return tasks
            else:
                return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = get_user_model().objects.all()
        context['stages'] = Stage.objects.all()
        return context

class TaskDetailView(StaffRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'tracker/task_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = get_user_model().objects.all()
        context['stages'] = Stage.objects.all()
        return context

#region task api

@staff_member_required
def newTask(request):
    context = {
        'workers': get_user_model().objects.all(),
        'stages': Stage.objects.all(),
    }
    return render(request, 'tracker/task_new.html', context)

@staff_member_required
def newTaskApi(request):
    worker = get_object_or_404(get_user_model(), pk=int(request.POST['receiver']))
    worker.task_set.create(
        pub_date=timezone.now(),
        due_date=request.POST['due_date'],
        status=get_object_or_404(Stage, pk=int(request.POST['status'])),
        title=request.POST['title'],
        desc=request.POST['desc'],
        file=request.FILES.get('file'),
        )
    worker.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))

@staff_member_required
def editTaskApi(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.desc = request.POST['desc']
    task.due_date=request.POST['due_date']
    task.status=get_object_or_404(Stage, pk=int(request.POST['status'])) 
    task.title=request.POST['title']
    task.desc=request.POST['desc']
    if (request.FILES.get('file')):
        task.file=request.FILES.get('file')
    worker = get_object_or_404(get_user_model(), pk=int(request.POST['receiver']))
    task.receiver = worker
    task.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))

@staff_member_required
def deleteTaskApi(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.status = 'deleted'
    task.save()
    return HttpResponseRedirect(reverse("tracker:worker-detail", args=(task.receiver.pk)))

@staff_member_required
def newStageApi(request):
    stage = Stage(title = request.POST['title'], color = request.POST['color'])
    print(request.POST['color'])
    stage.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))

@staff_member_required
def deleteStageApi(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    if (len(stage.task_set.all()) == 0):
        stage.delete()
    return HttpResponseRedirect(reverse("tracker:task-list"))

@login_required(login_url='/tasks/login/')
def advanceTaskApi(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    stages = get_list_or_404(Stage)
    index = stages.index(task.status)
    task.status = stages[index+1]
    task.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))

@login_required(login_url='/tasks/login/')
def retractTaskApi(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    stages = get_list_or_404(Stage)
    index = stages.index(task.status)
    task.status = stages[index-1]
    task.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))

@login_required(login_url='/tasks/login/')
def commentApi(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.comment_set.create(
        author = request.user,
        content = request.POST['content']
    )
    task.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))

#endregion

class WorkerDetailView(StaffRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = 'tracker/worker_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = get_user_model().objects.all()
        context['stages'] = Stage.objects.all()
        return context

#region login api

def loginApi(request):
    if (request.method == "POST"):
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(request, username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return redirect('tracker:task-list')
        else:
            return redirect('tracker:login-form')
    return render(request, 'tracker/login.html')

@login_required(login_url='/tasks/login/')
def logoutApi(request):
    logout(request)
    return redirect('tracker:login-form')
    
#endregion

class FilterDateView(generic.ListView):
    model = Task
    template_name = 'tracker/task_list.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.filter(due_date__day=self.kwargs['day']).filter(due_date__month=self.kwargs['month'])

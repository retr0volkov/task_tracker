from django.http import HttpResponse
from .models import Task, Worker
from django.shortcuts import get_list_or_404, render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class TaskListView(generic.ListView):
    template_name = 'tracker/task_list.html'
    context_object_name = 'tasks'
    queryset = Task.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = Worker.objects.all()
        return context

class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'tracker/task_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = Worker.objects.all()
        return context

#region task api

def newTaskApi(request):
    worker = get_object_or_404(Worker, pk=int(request.POST['receiver']))
    worker.task_set.create(
        pub_date=timezone.now(),
        due_date=request.POST['due_date'],
        status=request.POST['status'],
        title=request.POST['title'],
        desc=request.POST['desc'],
        )
    worker.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))
  
def editTaskApi(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.desc = request.POST['desc']
    task.due_date=request.POST['due_date']
    task.status=request.POST['status']
    task.title=request.POST['title']
    task.desc=request.POST['desc']
    worker = get_object_or_404(Worker, pk=int(request.POST['receiver']))
    task.receiver = worker
    task.save()
    return HttpResponseRedirect(reverse("tracker:task-list"))

def deleteTaskApi(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.status = 'deleted'
    task.save()
    return HttpResponseRedirect(reverse("tracker:worker-detail", args=(task.receiver.pk)))

#endregion

class WorkerListView(generic.ListView):
    template_name = 'tracker/worker_list.html'
    context_object_name = 'workers'
    queryset = Worker.objects.all()

class WorkerDetailView(generic.DetailView):
    model = Worker
    template_name = 'tracker/worker_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers'] = Worker.objects.all()
        return context

#region workers api

def newWorkerApi(request):
    worker = Worker(title = request.POST['title'])
    worker.save()
    return HttpResponseRedirect(reverse("tracker:worker-list"))

def editWorkerApi(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker.title = request.POST['title']
    worker.save()
    return HttpResponseRedirect(reverse("tracker:worker-detail", args=(worker.id)))

def deleteWorkerApi(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker.delete()
    return HttpResponseRedirect(reverse("tracker:worker-list", args=(worker.id)))
    
#endregion

class FilterDateView(generic.ListView):
    model = Task
    template_name = 'tracker/task_list.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.filter(due_date__day=self.kwargs['day']).filter(due_date__month=self.kwargs['month'])
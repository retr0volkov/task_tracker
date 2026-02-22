from django.http import HttpResponse
from .models import Task, Worker
from django.shortcuts import get_list_or_404, render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
	template_name = 'tracker/tasks_view.html'
	context_object_name = 'tasks'

	def get_queryset(self):
		return get_list_or_404(Task)

class TaskView(generic.DetailView):
    model = Task
    template_name = 'tracker/task_detail.html'
    

class FilteredWorkerView(generic.ListView):
	model = Task
	template_name = 'tracker/tasks_view.html'
	context_object_name = 'tasks'

	def get_queryset(self):
		return get_list_or_404(Task, receiver_id=self.kwargs['worker_id'])

class FilteredDueView(generic.ListView):
	model = Task
	template_name = 'tracker/tasks_view.html'
	context_object_name = 'tasks'

	def get_queryset(self):
		return get_list_or_404(Task) # filter by due date

class WorkerView(generic.ListView):
	model = Worker
	template_name = 'tracker/worker_view.html'
	context_object_name = 'workers'
 
	def get_queryset(self):
		return get_list_or_404(Worker)

def new_worker(request):
    # create new worker here
    w = Worker(title = request.POST['title'])
    w.save()
    return HttpResponseRedirect(reverse("tracker:index"))

def new_task(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker.task_set.create(
        pub_date=timezone.now(),
        due_date=request.POST['due_date'],
        status=request.POST['status'],
        title=request.POST['title'],
        desc=request.POST['desc'],
        )
    worker.save()
    return HttpResponseRedirect(reverse("tracker:filter-worker", args=(worker.id,)))
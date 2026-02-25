from django.urls import path

from . import views

app_name = 'tracker'
urlpatterns = [
    path("", views.TaskListView.as_view(), name='task-list'),
    path("<int:pk>/", views.TaskDetailView.as_view(), name='task-detail'),
    path("worker/", views.WorkerListView.as_view(), name='worker-list'),
    path("worker/<int:pk>/", views.WorkerDetailView.as_view(), name='worker-detail'),
    path("new/", views.newTaskApi, name='new-task'),
    path("edit/<int:task_id>/", views.editTaskApi, name='edit-task'),
    path("delete/<int:task_id>/", views.deleteTaskApi, name='delete-task'),
    path("worker/new/", views.newWorkerApi, name='new-worker'),
    path("worker/edit/<int:worker_id>/", views.editWorkerApi, name='edit-worker'),
    path("worker/delete/<int:worker_id>/", views.deleteWorkerApi, name='delete-worker'),
    path("<int:day>/<int:month>/", views.FilterDateView.as_view(), name='task-filter-date')
]
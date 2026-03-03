from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'tracker'
urlpatterns = [
    path("", views.TaskListView.as_view(), name='task-list'),
    path("<int:pk>/", views.TaskDetailView.as_view(), name='task-detail'),
    path("worker/", views.WorkerListView.as_view(), name='worker-list'),
    path("worker/<int:pk>/", views.WorkerDetailView.as_view(), name='worker-detail'),
    path("create/", views.newTask, name='create-task'),
    path("new/", views.newTaskApi, name='new-task'),
    path("edit/<int:task_id>/", views.editTaskApi, name='edit-task'),
    path("delete/<int:task_id>/", views.deleteTaskApi, name='delete-task'),
    path("advace/<int:task_id>/", views.advanceTaskApi, name='advance-task'),
    path("retract/<int:task_id>/", views.retractTaskApi, name='retract-task'),
    path("stage/new/", views.newStageApi, name='new-stage'),
    path("stage/delete/<int:stage_id>/", views.deleteStageApi, name='delete-stage'),
    path("worker/new/", views.newWorkerApi, name='new-worker'),
    path("worker/edit/<int:worker_id>/", views.editWorkerApi, name='edit-worker'),
    path("worker/delete/<int:worker_id>/", views.deleteWorkerApi, name='delete-worker'),
    path("<int:day>/<int:month>/", views.FilterDateView.as_view(), name='task-filter-date')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
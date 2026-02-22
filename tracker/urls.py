from django.urls import path

from . import views

app_name = 'tracker'
urlpatterns = [
    # ex: /tasks/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /tasks/1
    path("<int:pk>/", views.TaskView.as_view(), name="detail"),
    # ex: /tasks/filter/worker/1
    path("filter/worker/<int:worker_id>/", views.FilteredWorkerView.as_view(), name="filter-worker"),
    # ex: /tasks/filter/due/3/2
    path("filter/due/<int:month>/<int:day>/", views.FilteredDueView.as_view(), name="filter-due-date"),
    # ex: /tasks/worker
    path('worker/', views.WorkerView.as_view(), name='workers'),
    # ex: /tasks/worker/new
    path('worker/new/', views.new_worker, name='new-worker'),
    # ex: /tasks/worker/1/new_task
    path('worker/<int:worker_id>/new_task/', views.new_task, name='new-task')
    # edit a task
    # delete a task
]
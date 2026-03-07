from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'tracker'
urlpatterns = [
    path("", views.TaskListView.as_view(), name='task-list'),
    path("login/", views.loginApi, name='login-form'),
    path("logout/", views.logoutApi, name='logout-api'),
    path("<int:pk>/", views.TaskDetailView.as_view(), name='task-detail'),
    path("worker/<int:pk>/", views.WorkerDetailView.as_view(), name='worker-detail'),
    path("worker/", views.WorkerListView.as_view(), name='worker-list'),
    path("worker/new/", views.newUserApi, name='worker-new'),
    path("worker/changepwd/<str:user>/", views.changePasswordApi, name='worker-cpwd'),
    path("worker/delete/<str:user>/", views.deleteUserApi, name='worker-delete'),
    path("create/<int:stage_id>/", views.newTask, name='create-task'),
    path("new/", views.newTaskApi, name='new-task'),
    path("edit/<int:task_id>/", views.editTaskApi, name='edit-task'),
    path("delete/<int:task_id>/", views.deleteTaskApi, name='delete-task'),
    path("advace/<int:task_id>/", views.advanceTaskApi, name='advance-task'),
    path("retract/<int:task_id>/", views.retractTaskApi, name='retract-task'),
    path("comment/<int:task_id>/", views.commentApi, name='post-comment'),
    path("delete/<int:task_id>/", views.deleteTaskApi, name='task-delete'),
    path("stage/new/", views.newStageApi, name='new-stage'),
    path("stage/delete/<int:stage_id>/", views.deleteStageApi, name='delete-stage'),
    path("<int:day>/<int:month>/", views.FilterDateView.as_view(), name='task-filter-date')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
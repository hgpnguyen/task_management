from django.urls import path
from .views import TaskListView, TaskDetailView


urlpatterns = [
    path('', TaskListView.as_view()), # Path: /tasks/?page=<int:page>&page_size=<int:page_size>&status=<str:status>
    path('<int:task_id>/', TaskDetailView.as_view()) # Path: /tasks/<int:task_id>/
]

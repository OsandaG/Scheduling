from django.urls import path

how from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="Home"),
    path("ListTask", views.TaskListView.as_view(), name="List Tasks"),
    path("ListTimeEntry", views.TaskListView.as_view(), name="List Time Entries"),
    path("UpdateTask/<int:pk>/", views.TaskUpdateView.as_view() , name="Update Task"),
    path("UpdateTimeEntry/<int:pk>/", views.TimeEntryUpdateView.as_view() , name="Update Time Entry"),
    path("CreateTask", views.TaskCreateView.as_view(), name="Create Task"),
    path("CreateTimeEntry", views.TimeEntryCreateView.as_view(), name="Create Time Entry"),
    path("action/<action>/<id>", views.Actions.as_view(), name="my-view"),
]
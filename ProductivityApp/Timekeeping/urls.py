from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="Home"),
    path("ListTask", views.TaskListView.as_view(), name="List Tasks"),
    path("ListTimeEntry", views.TimeEntryListView.as_view(), name="List Time Entries"),
    path("UpdateTask/<int:pk>/", views.TaskUpdateView.as_view() , name="Update Task"),
    path("UpdateTimeEntry/<int:pk>/", views.TimeEntryUpdateView.as_view() , name="Update Time Entry"),
    path("DeleteTask/<int:pk>/", views.TaskDeleteView.as_view(), name="Delete Task"),
    path("DeleteTimeEntry/<int:pk>/", views.TimeEntryDeleteView.as_view(), name="Delete Time Entry"),
    path("CreateTask", views.TaskCreateView.as_view(), name="Create Task"),
    path("CreateTimeEntry", views.TimeEntryCreateView.as_view(), name="Create Time Entry"),
    path("action/<action>/<id>", views.TaskActions.as_view(), name="actions"),
    path("general_actions/<action>", views.GeneralActions.as_view(), name="general_tasks")
]
from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from .models import Task, TimeEntry
from .forms import TaskCRUDForm, TimeEntryCRUDForm
from django.forms.models import model_to_dict
from django.views import View
from django.shortcuts import redirect


def url_list():
    urlpatterns = ['Home', 'List Tasks', 'List Time Entries', 'Create Task', 'Create Time Entry']
    link_list = []
    for name in urlpatterns:
        url_name_dict = {}
        url_name_dict['name'] = name
        url_name_dict['link'] = reverse_lazy(name)
        link_list.append(url_name_dict)
    return link_list


class TaskListView(ListView):
    model = Task
    template_name = 'generic_list.html'

    def get_queryset(self):
        object_list = []
        for res in super().get_queryset():
            res_dict = OrderedDict(model_to_dict(res))
            name = res_dict.pop('name')
            id = res_dict.pop('id')
            notes = res_dict.pop('task_notes')

            notes = f"""
            <div class="text-wrap" style="width: 30rem;">
                {notes[:min(len(notes), 200)]}</div>
            """

            html_element = f"""
            <span class="badge rounded-pill text-bg-primary">
            <a class="badge" aria-current="page" href="/UpdateTask/{id}">{name}</a></span>
            """
            res_dict['Name'] = html_element
            res_dict.move_to_end("Name", last=False)
            res_dict['Task Notes'] = notes
            res_dict['Controls'] = f"""
            <a href="action/play/{id}"><i class="bi bi-play-circle" style="font-size: 2rem; color: cornflowerblue;"></i></a>
            <a href="action/pause/{id}"><i class="bi bi-pause-circle" style="font-size: 2rem; color: cornflowerblue;"></i></a>
            <a href="action/next/{id}"><i class="bi bi-fast-forward-circle" style="font-size: 2rem; color: cornflowerblue;"></i></a>
            <a href="action/completed/{id}"><i class="bi bi-award" style="font-size: 2rem; color: cornflowerblue;"></i></a>
            """
            # <a href="https://example.com"><i class="bi bi-app"></i>
            object_list.append(res_dict)
        return object_list

    def get_context_data(self, **kwargs):
        # Call the superclass method to get the default context data
        context = super().get_context_data(**kwargs)
        toast = self.request.session.pop('error_message', None)
        if toast:
            context['toast'] = toast

        # Add additional variables to the context
        context['title'] = 'Task List'
        context['nav_bar'] = url_list()

        return context


class TimeEntryListView(ListView):
    model = TimeEntry
    template_name = 'generic_list.html'


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Tasks')


class TimeEntryUpdateView(UpdateView):
    model = TimeEntry
    form_class = TimeEntryCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Time Entries')


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Tasks')


class TimeEntryCreateView(CreateView):
    model = TimeEntry
    form_class = TimeEntryCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Time Entries')


class Actions(View):
    def get(self, request, action, id, *args, **kwargs):
        self.request = request
        if action == 'play':
            self.play(id)
        elif action == 'pause':
            self.pause(id)
        elif action == 'next':
            self.next(id)
        elif action == 'completed':
            self.completed(id)
        return redirect('Home')

    def play(self, id):
        """
        Task with id=id marked as Running
        Other running tasks marked as paused
        Create New time Entry for Task with id=id
        Other running tasks Time entries updated.
        :param id:
        :return:
        """
        current_task = Task.objects.get(pk=id)
        other_tasks = Task.objects.filter(id=id,status='Running')
        if current_task.status in ('Running', 'Complete', 'Deferred'):
            self.request.session['error_message'] = f'{current_task.name} cannot be started'
        for task in other_tasks:
            time_entries = TimeEntry.objects.filter(task=task, end_time__isnull=True)
            #for time
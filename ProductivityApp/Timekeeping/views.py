from collections import OrderedDict
from datetime import datetime, timezone, timedelta

from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView

from .forms import TaskCRUDForm, TimeEntryCRUDForm, DateForm
from .models import Task, TimeEntry
from django.views.generic.edit import DeleteView


class ViewMixIn:
    def get_context_data(self, **kwargs):
        # Call the superclass method to get the default context data
        context = super().get_context_data(**kwargs)
        updates = self.request.session.pop('updates', None)
        if updates:
            context['updates'] = updates

        # Add additional variables to the context
        context['title'] = 'Task List'
        context['nav_bar'] = self.url_list()

        return context

    def url_list(self):
        urlpatterns = ['List Tasks', 'List Time Entries', 'Create Task', 'Create Time Entry']
        link_list = []
        for name in urlpatterns:
            url_name_dict = {}
            url_name_dict['name'] = name
            url_name_dict['link'] = reverse_lazy(name)
            link_list.append(url_name_dict)
        return link_list


class HomeView(ViewMixIn, ListView):
    model = Task
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Call the superclass method to get the default context data
        context = super().get_context_data(**kwargs)
        initial_show_date = self.request.GET.get('show_date',None)
        if not initial_show_date:
            initial_show_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

        context['filter_form'] = DateForm(initial={'show_date': initial_show_date})
        return context

    def get_filtered_tasks(self):
        form = DateForm(self.request.GET)

        if form.is_valid():
            show_date = form.cleaned_data.get('show_date')

            if show_date:
                queryset = Task.objects.filter(task_date=show_date)  # Modify as per your model fields
            else:
                queryset = Task.objects.filter(task_date=datetime.strftime(datetime.now(), '%Y-%m-%d'))  # Modify as per your model fields

        return queryset

    def get_queryset(self):
        object_list = []
        task_list = self.get_filtered_tasks()
        for res in task_list:
            # <a href="https://example.com"><i class="bi bi-app"></i>

            time_used = self.get_used_time(res)
            assigned_seconds = res.get_assigned_seconds()
            res_dict = {
                'Name': self.get_edit_badge(res),
                'Proposed Time': res.start,
                'Assigned Time': f'{int(assigned_seconds // 60)}M {int(assigned_seconds) % 60}S',
                'Used Time': f'{time_used // 60}M {int(time_used) % 60}S',
                'Task Notes': self.concat_notes(res),
                'Status': self.get_status_html(res),
                'Controls': self.get_controls(res.id),
                'Utility_Progress': self.get_progress(res.status, time_used, assigned_seconds),
                'Utility_Priority': self.get_priority_colour(res.priority)
            }
            object_list.append(res_dict)
        return object_list

    def get_priority_colour(self, priority):
        if priority == 'Normal':
            return 'table-default'
        elif priority == 'Urgent':
            return 'table-danger'
        else:
            return 'table-warning'

    def get_edit_badge(self, res):
        html_element = f"""
            <span class="badge rounded-pill text-bg-primary fs-4">
            <a class="badge" aria-current="page" href="/UpdateTask/{res.id}">{res.name}</a></span>
            """
        return html_element

    def get_progress(self, status, time_used, assigned_seconds):
        if status == 'Completed':
            return 100
        else:
            return int(100 * time_used / assigned_seconds)

    def get_used_time(self, res):
        time_entries = TimeEntry.objects.filter(task__id=res.id)
        time_used = 0
        for time_entry in time_entries:
            if time_entry.duration:
                time_used += time_entry.duration
            else:
                used_time = (datetime.now(timezone.utc) - time_entry.start_time).total_seconds()
                time_used += used_time
        return time_used

    def get_status_html(self, res):
        if res.status == 'Running':
            status_html = f"""<div class = "text-center">
                            <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Task Running...</span>
                            </div>
                            <p class="text-break">{res.status}</p>
                            </div>
                            """
        elif res.status == 'Completed':
            status_html = f"""<div class = "text-center">
                            <i class="bi bi-check-circle-fill" style="font-size: 2rem; color: cornflowerblue;"></i>
                            <p class="text-break">{res.status}</p>
                            </div>"""
        elif res.status == 'Not Started':
            status_html = f"""<div class = "text-center">
                            <i class="bi bi-circle" style="font-size: 2rem; color: cornflowerblue;"></i>
                            <p class="text-break">{res.status}</p>
                            </div>"""
        else:
            status_html = f"""<div class = "text-center">
                            <div class="spinner-grow text-primary" style="animation-duration: 7s;" role="status">
                            <span class="visually-hidden">Task Running...</span>
                            </div>
                            <p class="text-break">{res.status}</p>
                            </div>
                            """
        return status_html

    def get_controls(self, id):
        return f"""
            <a href="action/play/{id}" ><i class="bi bi-play-circle" style="font-size: 3rem;" aria-disabled="true"></i></a>
            <a href="action/pause/{id}"><i class="bi bi-pause-circle" style="font-size: 3rem; color: cornflowerblue;"></i></a>
            <a href="action/next/{id}"><i class="bi bi-fast-forward-circle" style="font-size: 3rem; color: cornflowerblue;"></i></a>
            <a href="action/completed/{id}"><i class="bi bi-award" style="font-size: 3rem; color: cornflowerblue;"></i></a>
            """

    def concat_notes(self, res):
        notes = res.task_notes
        return f"""
            <div class="text-wrap" style="width: 20rem;">
            {notes[:min(len(notes), 200)]}</div>
            """

def reset(request):
    Task.objects.all().delete()
    TimeEntry.objects.all().delete()
    return HttpResponse("All Deleted")

class TaskDeleteView(ViewMixIn,DeleteView):
    model = Task
    success_url = reverse_lazy("List Tasks")
    template_name = 'check_delete.html'

class TimeEntryDeleteView(ViewMixIn,DeleteView):
    model = TimeEntry
    success_url = reverse_lazy("List Time Entries")
    template_name = 'check_delete.html'


class TaskListView(ViewMixIn, ListView):
    model = Task
    template_name = 'generic_list.html'

    def get_queryset(self):
        object_list = []
        for res in super().get_queryset():
            res_dict = OrderedDict(model_to_dict(res))
            res_dict['Edit'] = f"""
            <span class="badge rounded-pill text-bg-primary fs-4">
            <a class="badge" aria-current="page" href="/UpdateTask/{res.id}">{res.__str__()}</a></span>
            """
            res_dict['Delete'] = f"""
             <span class="badge rounded-pill text-bg-primary fs-4">
             <a class="badge" aria-current="page" href="/DeleteTask/{res.id}">{res.__str__()}</a></span>
             """
            object_list.append(res_dict)
        return object_list

class TimeEntryListView(ViewMixIn, ListView):
    model = TimeEntry
    template_name = 'generic_list.html'

    def get_queryset(self):
        object_list = []
        for res in super().get_queryset():
            res_dict = OrderedDict(model_to_dict(res))
            res_dict['Edit'] = f"""
            <span class="badge rounded-pill text-bg-primary fs-4">
            <a class="badge" aria-current="page" href="/UpdateTimeEntry/{res.id}">{res.__str__()}</a></span>
            """
            res_dict['Edit'] = f"""
             <span class="badge rounded-pill text-bg-primary fs-4">
             <a class="badge" aria-current="page" href="/UpdateTimeEntry/{res.id}">{res.__str__()}</a></span>
             """
            object_list.append(res_dict)
        return object_list


class TaskUpdateView(ViewMixIn,UpdateView):
    model = Task
    form_class = TaskCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Tasks')


class TimeEntryUpdateView(ViewMixIn,UpdateView):
    model = TimeEntry
    form_class = TimeEntryCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Time Entries')


class TaskCreateView(ViewMixIn,CreateView):
    model = Task
    form_class = TaskCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Tasks')


class TimeEntryCreateView(ViewMixIn,CreateView):
    model = TimeEntry
    form_class = TimeEntryCRUDForm
    template_name = 'generic_create_update.html'
    success_url = reverse_lazy('List Time Entries')


class Actions(View):
    def get(self, request, action, id, *args, **kwargs):
        self.request = request
        self.request.session['updates'] = list()
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
        other_tasks = Task.objects.filter(id=id, status='Running')
        _now = datetime.now(timezone.utc)
        if other_tasks.count() > 1:
            self.request.session['updates'].append(('error', f'More than 1 running task found, closing others!'))
        if current_task.status in ('Running', 'Complete', 'Deferred'):
            self.request.session['updates'].append(('error', f'{current_task.name} cannot be started'))
            return
        for task in other_tasks:
            time_entries = TimeEntry.objects.filter(task=task, end_time__isnull=True)
            if time_entries.count() > 1:
                self.request.session['updates'].append(('error', f'Too many open time entries for {task.name}'))
            for time_entry in time_entries:
                time_entry.close_entry()
            task.status = 'Paused'
            task.save()

        new_time_entry = TimeEntry.objects.create(task=current_task, start_time=_now)
        current_task.used_time.add(new_time_entry)
        current_task.status = 'Running'
        current_task.save()
        self.request.session['updates'].append(('info', f"{current_task.name} is now running."))

    def pause(self, id):
        current_task = Task.objects.get(pk=id)

        time_entries = TimeEntry.objects.filter(task=current_task, end_time__isnull=True)
        _now = datetime.now(timezone.utc)
        if time_entries.count() > 1:
            self.request.session['updates'].append(('error', f'Too many open time entries for {current_task.name}'))
        for time_entry in time_entries:
            time_entry.close_entry(_now)
        current_task.status = 'Paused'
        current_task.save()
        self.request.session['updates'].append(('info', f"{current_task.name} has been paused."))

    def next(self, id):
        current_task = Task.objects.get(pk=id)
        time_entries = TimeEntry.objects.filter(task=current_task, end_time__isnull=True)
        _now = datetime.now(timezone.utc)
        if time_entries.count() > 1:
            self.request.session['updates'].append(('error', f'Too many open time entries for {current_task.name}'))
        for time_entry in time_entries:
            time_entry.close_entry(_now)
        tomorrow = _now + timedelta(days=1)
        current_task.task_date = tomorrow.date()
        current_task.save()
        self.request.session['updates'].append(('info', f"{current_task.name} has been moved to tomorrow."))

    def completed(self, id):
        current_task = Task.objects.get(pk=id)
        time_entries = TimeEntry.objects.filter(task=current_task, end_time__isnull=True)
        _now = datetime.now(timezone.utc)
        if time_entries.count() > 1:
            self.request.session['updates'].append(('error', f'Too many open time entries for {current_task.name}'))
        for time_entry in time_entries:
            time_entry.close_entry(_now)
        current_task.status = 'Completed'
        tomorrow = _now + timedelta(days=1)
        current_task.task_date = tomorrow.date()
        current_task.save()
        self.request.session['updates'].append(('info', f"{current_task.name} has been marked as complete."))

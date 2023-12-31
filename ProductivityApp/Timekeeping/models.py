from django.db import models


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_date = models.DateField(auto_now=True, verbose_name="Created Date", blank=True, null=True)
    task_date = models.DateField(verbose_name="Task Date", blank=True, null=True)
    start = models.TimeField(verbose_name="Proposed Start Time", blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name="Task Name", blank=True, null=True)
    assigned_time = models.TimeField(verbose_name="Assigned Time", blank=True, null=True)
    priority_choices = [
        ('Urgent', 'Urgent'),
        ('Normal', 'Normal'),
        ('Low', 'Low'),
    ]
    priority = models.CharField(max_length=30, choices=priority_choices, blank=True, null=True)

    task_notes = models.TextField(verbose_name="Task Notes", blank=True, null=True)
    status_choices = [
        ('Running', 'Running'),
        ('Paused', 'Paused'),
        ('Completed', 'Completed'),
        ('Not Started', 'Not Started'),
        ('Deferred', 'Deferred'),
    ]
    status = models.CharField(max_length=30, choices=status_choices, blank=True, null=True)
    used_time = models.ManyToManyField("TimeEntry", blank=True, null=True, verbose_name='Time Entries',
                                       related_name='time_entries')

    def __str__(self):
        return f"{self.created_date}-{self.name}"


class TimeEntry(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Task, models.SET_NULL, blank=True, null=True, verbose_name='Task')
    start_time = models.DateTimeField(verbose_name="Started Time", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="End Time", blank=True, null=True)
    duration = models.BigIntegerField(verbose_name="Duration", blank=True, null=True)

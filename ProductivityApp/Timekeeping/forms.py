from django import forms
from django.forms.widgets import DateInput

from .models import Task, TimeEntry  # Import your model


class TaskCRUDForm(forms.ModelForm):
    class Meta:
        model = Task  # Specify the model
        exclude = ['id', 'created_date']  # Specify the fields you want in the form
        widgets = {
            'task_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'task_notes': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'used_time': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'assigned_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }


class TimeEntryCRUDForm(forms.ModelForm):
    class Meta:
        model = TimeEntry  # Specify the model
        fields = '__all__'  # Specify the fields you want in the form
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duration': forms.TimeInput(attrs={'class': 'form-control', 'readonly': None}),
        }

    task = forms.ModelChoiceField(
        queryset=Task.objects.all(),  # Use the Author model as the queryset
        empty_label="Select Task",
        widget=forms.Select(attrs={'class': 'form-select'})

    )


class DateForm(forms.Form):
    # Define your form fields for filtering here
    show_date = forms.DateField(
        label='Show Date',
        widget=DateInput(attrs={'type': 'date'}),  # Use the DateInput widget
        required=False  # Add this if the field is optional
    )

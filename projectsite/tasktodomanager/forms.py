from django.forms import ModelForm
from django import forms
from .models import Task, SubTask, Note

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'category', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'status']

class SubTaskAddForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'subtask-input',
                'placeholder': 'Enter subtask title'
            }),
            'status': forms.Select(attrs={'class': 'subtask-select'}),
        }

class NoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'note-input',
                'rows': 4,
            }),
        }

class NoteAddForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']   
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'note-input',
                'placeholder': 'Write your note here...',
                'rows': 4,
            }),
        }
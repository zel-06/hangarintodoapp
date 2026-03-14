from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from tasktodomanager.models import Category, Task
from tasktodomanager.forms import TaskForm
from django.urls import reverse_lazy
from django.db.models import Q


class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"

class TaskListView(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_list.html'
    paginate_by = 5
    ordering = ['priority__name']

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')
from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tasktodomanager.models import Category, Task, Priority, SubTask, Note
from tasktodomanager.forms import TaskForm, TaskUpdateForm
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
import json


class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

class TaskListView(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        qs = Task.objects.select_related("category", "priority")

        # filter by category
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)

        # filter by priority
        priority_id = self.request.GET.get("priority")
        if priority_id:
            qs = qs.filter(priority_id=priority_id)

        return qs.order_by("category__name")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["priorities"] = Priority.objects.all()  # assuming you have a Priority model

        context["total_task"] = Task.objects.exclude(status="Completed").count()

        context["total_accomplished"] = Task.objects.filter(status="Completed").count()
        context["pending_total"] = Task.objects.filter(status="Pending").count()
        context["in_progress_total"] = Task.objects.filter(status="In Progress").count()

        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')
    
class SubtaskListView(ListView):
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'

    def get_queryset(self):
        # Use parent_task instead of task
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        return SubTask.objects.filter(parent_task=task)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['pk'])
        return context
    
class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        # Use task instead of parent_task
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        return Note.objects.filter(task=task)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['pk'])
        return context

class TaskDoneView(View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        data = json.loads(request.body)
        task.status = data.get("status", task.status)
        task.save()
        return JsonResponse({"id": task.id, "status": task.status})
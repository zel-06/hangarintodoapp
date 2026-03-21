from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tasktodomanager.models import Category, Task, Priority, SubTask, Note
from tasktodomanager.forms import TaskForm, TaskUpdateForm, SubTaskForm, SubTaskAddForm, NoteAddForm, NoteUpdateForm
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

#TASK
class TaskListView(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        qs = Task.objects.select_related("category", "priority")

        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)

        priority_id = self.request.GET.get("priority")
        if priority_id:
            qs = qs.filter(priority_id=priority_id)

        return qs.order_by("category__name")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["priorities"] = Priority.objects.all()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_page'] = self.request.GET.get('from', 'home')
        return context


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_page'] = 'dashboard'
        return context


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')


#SUBTASK   
class SubtaskListView(ListView):
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'

    def get_queryset(self):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return SubTask.objects.filter(parent_task=task)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return context
    
class SubtaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskAddForm
    template_name = 'subtask_add.html'

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        form.instance.parent_task = task
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('subtask-list', kwargs={'task_id': self.kwargs['task_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return context

class SubtaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(SubTask, pk=self.kwargs['subtask_id'])

    def get_success_url(self):
        return reverse_lazy('subtask-list', kwargs={'task_id': self.object.parent_task.id})

class SubtaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_del.html'

    def get_object(self, queryset=None):
        return get_object_or_404(SubTask, pk=self.kwargs['subtask_id'])

    def get_success_url(self):
        return reverse_lazy('subtask-list', kwargs={'task_id': self.kwargs['task_id']})


#NOTES
class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(task_id=self.kwargs['task_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return context
    
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteAddForm
    template_name = 'note_add.html'

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        form.instance.task = task
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notes-list', kwargs={'task_id': self.kwargs['task_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return context


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteUpdateForm
    template_name = 'note_form.html'
    context_object_name = 'note'

    def get_success_url(self):
        return reverse_lazy('notes-list', kwargs={'task_id': self.object.task.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object.task
        return context


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_del.html'
    context_object_name = 'note'

    def get_success_url(self):
        return reverse_lazy('notes-list', kwargs={'task_id': self.object.task.id})

class TaskDoneView(View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        data = json.loads(request.body)
        task.status = data.get("status", task.status)
        task.save()
        return JsonResponse({"id": task.id, "status": task.status})
    

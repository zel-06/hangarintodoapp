from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from tasktodomanager.models import Category, Task, CompletedTask, Priority
from tasktodomanager.forms import TaskForm
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone


class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"

class TaskListView(ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_list.html'
    paginate_by = 4
    
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
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class DashboardView(ListView):
    model = Task
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_task"] = Task.objects.count()

        category_counts = (
            Task.objects.values("category__name")
            .annotate(total=Count("category"))
            .order_by("-total")
        )
        if category_counts:
            top_category = category_counts[0]
            context["top_category_name"] = top_category["category__name"]
            context["top_category_total"] = top_category["total"]
        else:
            context["top_category_name"] = None
            context["top_category_total"] = 0

        today = timezone.now().date()
        count = Task.objects.filter(
            created_at__year=today.year
        ).count()
        
        context["task_created_this_year"] = count
        context["total_accomplished"] = CompletedTask.objects.filter(accomplished=True).count()

        return context
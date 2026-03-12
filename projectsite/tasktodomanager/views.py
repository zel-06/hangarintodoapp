from django.shortcuts import render

from django.views.generic.list import ListView
from tasktodomanager.models import Category, Task 

# Create your views here.
class HomePageView(ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"
"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasktodomanager.views import HomePageView, TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, SubtaskListView, NoteListView, TaskDoneView

from tasktodomanager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")), # allauth routes
    
    path('', views.HomePageView.as_view(), name='home'),

    #Task
    path('task_list/', TaskListView.as_view(), name='task-list'),
    path('task_list/add', TaskCreateView.as_view(), name='task-add'),
    path('task_list/<pk>', TaskUpdateView.as_view(), name='task-update'),
    path('task_list/<pk>/delete', TaskDeleteView.as_view(), name='task-delete'),

    #Subtask and Notes
    path('task_list/<pk>/subtask', SubtaskListView.as_view(), name='subtask-list'),
    path('task_list/<pk>/notes', NoteListView.as_view(), name='notes-list'),
    path('task_list/<pk>/done/', TaskDoneView.as_view(), name='task-done'),
]

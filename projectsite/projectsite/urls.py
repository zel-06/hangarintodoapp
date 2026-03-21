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
from tasktodomanager.views import HomePageView, TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, SubtaskListView, NoteListView, TaskDoneView, SubtaskUpdateView, SubtaskCreateView, SubtaskDeleteView, NoteCreateView, NoteUpdateView, NoteDeleteView

from tasktodomanager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    
    path('', views.HomePageView.as_view(), name='home'),

    #Task
    path('task_list/', TaskListView.as_view(), name='task-list'),
    path('task_list/add', TaskCreateView.as_view(), name='task-add'),
    path('task_list/<pk>', TaskUpdateView.as_view(), name='task-update'),
    path('task_list/<pk>/delete', TaskDeleteView.as_view(), name='task-delete'),

    #Subtask
    path('task_list/<int:task_id>/subtask/', SubtaskListView.as_view(), name='subtask-list'),
    path('task_list/<int:task_id>/subtask/add/', SubtaskCreateView.as_view(), name='subtask-add'),
    path('task_list/<int:task_id>/subtask/<int:subtask_id>/edit/', SubtaskUpdateView.as_view(), name='subtask-update'),
    path('task_list/<int:task_id>/subtask/<int:subtask_id>/delete/', SubtaskDeleteView.as_view(), name='subtask-delete'),

    #Notes
    path('task_list/<int:task_id>/notes/', NoteListView.as_view(), name='notes-list'),
    path('task_list/<int:task_id>/notes/add/', NoteCreateView.as_view(), name='note-add'),
    path('task_list/<int:task_id>/notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='note-update'),
    path('task_list/<int:task_id>/notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),

    path('task_list/<pk>/done/', TaskDoneView.as_view(), name='task-done'),
]

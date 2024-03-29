from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'baseApp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        # Get the current logged-in user
        user = self.request.user
        # Filter tasks by the current user (sql query with WHERE statement is executed under the hood)
        queryset = Task.objects.filter(user=user)
        return queryset

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'baseApp/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # field = ['title', 'description']
    fields = ['title', 'description','location', 'completed']
    # Redirect to tasks list when task created correctly
    success_url = reverse_lazy('tasks') 
    
    # Method is called when the form is valid, and it's where you can customize what happens when a new task is created 
    def form_valid(self, form):
        # Set the user of the task to the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description','location', 'completed']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    # Custom object name in template
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks')

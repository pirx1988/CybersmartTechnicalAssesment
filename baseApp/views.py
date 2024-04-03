from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import requests
import logging

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from weatherMapApi.utils import fetchWeather, calcBackgroundColor

DEFAULT_BACKGROUND_COLOR = '#FFFFFF'  # Example default color (white)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'baseApp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'baseApp/task_list.html'

    def get_queryset(self):
        # Get the current logged-in user
        user = self.request.user
        # Filter tasks by the current user (sql query with WHERE statement is executed under the hood)
        queryset = Task.objects.filter(user=user)
        for task in queryset:
            try:
                response = fetchWeather(task.location)
                json_response = response.json()
                weather = json_response['weather'][0]['main']
                # Temperature in celsius degress of selected location
                temp = json_response['main']['temp']
                task.background_color = calcBackgroundColor(weather, temp)
            except requests.HTTPError as e:
                # Handle HTTPError (response status code is not 200)
                # provide a default value for background color
                logger.error(
                    f"HTTPError occurred  while fetching weather data from weatherMap Api for task with id {task.id}")
                task.background_color = DEFAULT_BACKGROUND_COLOR
            except Exception as e:
                # Handle other exceptions (e.g., network errors)
                # provide a default value for background color
                logger.error(
                    f"An error occurred while fetching weather data from weatherMap Api for task with id: {task.id}")
                task.background_color = DEFAULT_BACKGROUND_COLOR
        return queryset


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'baseApp/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # field = ['title', 'description']
    fields = ['title', 'description', 'location', 'completed']
    # Redirect to tasks list when task created correctly
    success_url = reverse_lazy('tasks')

    # Method is called when the form is valid, and it's where you can customize what happens when a new task is created
    def form_valid(self, form):
        # Set the user of the task to the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'location', 'completed']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    # Custom object name in template
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

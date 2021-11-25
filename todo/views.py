from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from todo.models import Task


class TaskView(CreateView):
    model = Task
    fields = ['details', 'owner']
    template_name = 'todo/todo.html'
    success_url = reverse_lazy('todo:todo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = Task.objects.filter(is_done=False, archive=False)
        return context


class ArchiveTaskView(View):

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.archive = True
        task.save()
        return HttpResponseRedirect(reverse('todo:todo'))

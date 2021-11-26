from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
from todo.models import Task


class TaskView(LoginRequiredMixin, CreateView):
    login_url = 'admin:index'
    model = Task
    fields = ['title', 'details']
    template_name = 'todo/todo.html'
    success_url = reverse_lazy('todo:todo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match self.kwargs.get("filter", None):
            case "all":
                context['task_list'] = Task.objects.filter(archive=False)
            case "done":
                context['task_list'] = Task.objects.filter(
                    is_done=True, archive=False)
            case _:
                context['task_list'] = Task.objects.filter(
                    is_done=False, archive=False)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ArchiveTaskView(View):

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.archive = True
        task.save()
        return HttpResponseRedirect(reverse('todo:todo'))


class DoneTaskView(View):

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.is_done = True
        task.save()
        return HttpResponseRedirect(reverse('todo:todo'))

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse, resolve
from django.views import View
from django.views.generic import CreateView
from todo.models import Task


class TaskView(LoginRequiredMixin, CreateView):
    login_url = 'user:login'
    model = Task
    fields = ['title', 'details']
    template_name = 'todo/todo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        match self.kwargs.get("filter", None):
            case "all":
                context['task_list'] = Task.objects.filter(
                    archive=False, owner_id=user.id)
            case "done":
                context['task_list'] = Task.objects.filter(
                    is_done=True, archive=False, owner_id=user.id)
            case _:
                context['task_list'] = Task.objects.filter(
                    is_done=False, archive=False, owner_id=user.id)
        return context

    def get_success_url(self):
        return reverse_lazy(
            'todo:filter',
            kwargs={"filter": self.kwargs.get("filter", None)}
        )

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ArchiveTaskView(View):

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.owner == request.user or request.user.is_superuser:
            task.archive = True
            task.save()
        return HttpResponseRedirect(reverse('todo:todo'))


class DoneTaskView(View):

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.owner == request.user or request.user.is_superuser:
            task.is_done = True
            task.save()
        return HttpResponseRedirect(reverse('todo:todo'))

from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Value
from django.db.models.functions import Now
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from todo.models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'details', 'deadline']
    template_name = 'todo/todo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        selection = self.kwargs.get("selection", None)
        match selection:
            case "all":
                context['task_list'] = Task.objects.filter(
                    archive=False, owner_id=user.id).annotate(
                    time_left=F("deadline") - Now())
            case "done":
                context['task_list'] = Task.objects.filter(
                    is_done=True, archive=False, owner_id=user.id).annotate(
                    time_left=Value(timedelta(days=2)))
            case _:
                context['task_list'] = Task.objects.filter(
                    is_done=False, archive=False, owner_id=user.id).annotate(
                    time_left=F("deadline") - Now())
        context["selection"] = selection
        return context

    def get_success_url(self):
        return reverse_lazy(
            'todo:filter',
            kwargs={"filter": self.kwargs.get("filter", None)}
        )

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ArchiveTaskView(LoginRequiredMixin, View):

    def post(self, request, selection, pk):
        task = Task.objects.get(pk=pk)
        if task.owner == request.user or request.user.is_superuser:
            task.archive = True
            task.save()
        return HttpResponseRedirect(reverse_lazy(
            'todo:filter',
            kwargs={"filter": selection})
        )


class DoneTaskView(LoginRequiredMixin, View):

    def post(self, request, pk, selection):
        task = Task.objects.get(pk=pk)
        if task.owner == request.user or request.user.is_superuser:
            task.is_done = True
            task.save()
        return HttpResponseRedirect(reverse_lazy(
            'todo:filter',
            kwargs={"filter": selection})
        )


class UndoDoneTaskView(LoginRequiredMixin, View):

    def post(self, request, pk, selection):
        task = Task.objects.get(pk=pk)
        if task.owner == request.user or request.user.is_superuser:
            task.is_done = False
            task.save()
        return HttpResponseRedirect(reverse_lazy(
            'todo:filter',
            kwargs={"filter": selection})
        )

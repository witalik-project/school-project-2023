from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Classes, PointsLog, Article
from .forms import (
    ArticlesCreateEditForm,
    ClassesEditExceptPointsForm,
    PointsLogCreateForm,
    PointsAddSubtractLogCreateEditForm,
    ClassesCreateEditForm,
)
from .filters import PointsLogFilter


class Index(ListView):
    template_name = "index.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latests_articles'] = Article.objects.order_by("-published_date")[:4]
        return context


class CreateArticle(LoginRequiredMixin, CreateView):
    template_name = "create/create_article.html"
    model = Article
    form_class = ArticlesCreateEditForm
    success_url = "/"


class EditArticle(LoginRequiredMixin, UpdateView):
    template_name = "edit/edit_article.html"
    model = Article
    form_class = ArticlesCreateEditForm
    success_url = "/"


class DeleteArticle(LoginRequiredMixin, DeleteView):
    template_name = "delete/delete_article.html"
    model = Article
    success_url = "/"


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.add_message(request, messages.INFO, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.add_message(
                    request, messages.ERROR, "Nieprawidłowa nazwa użytkownika lub hasło"
                )
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="registration/login.html",
        context={"login_form": form},
    )


def logout_request(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request=request, template_name="registration/logout.html")


class ClassesList(ListView):
    template_name = "classes_list.html"
    model = Classes
    context_object_name = "classes"


class CreateClass(LoginRequiredMixin, CreateView):
    template_name = "create/create_class.html"
    model = Classes
    form_class = ClassesCreateEditForm
    success_url = "/school/classes"


class EditClass(LoginRequiredMixin, UpdateView):
    template_name = "edit/edit_class.html"
    model = Classes
    form_class = ClassesEditExceptPointsForm
    success_url = "/school/classes"


class DeleteClass(LoginRequiredMixin, DeleteView):
    template_name = "delete/delete_class.html"
    model = Classes
    success_url = "/school/classes"


@login_required
def create_points_log(request):
    if request.method == "POST":
        form = PointsLogCreateForm(request.POST)
        if form.is_valid():
            log = PointsLog(
                points_log_class=form.cleaned_data["points_log_class"],
                points_log_type=form.cleaned_data["points_log_type"],
                points_log_amount=form.cleaned_data["points_log_amount"],
                points_log_created_by=request.user,
            )
            print(log.points_log_type)
            if log.points_log_type:
                add_check = log.points_log_class.class_points + log.points_log_amount
                if add_check > 1000:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"Nie można dodać tej ilości punktów. Teraz {log.points_log_class.class_number}{log.points_log_class.class_letter} klasa ma: {log.points_log_class.class_points}/1000 punktów",
                    )
                else:
                    print(log.points_log_type)
                    log.points_log_class.class_points = (
                        log.points_log_class.class_points + log.points_log_amount
                    )
                    log.points_log_class.save()
                    log.save()
                    return HttpResponseRedirect("/")
            else:
                subtract_check = (
                    log.points_log_class.class_points - log.points_log_amount
                )
                if subtract_check < 0:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f"Nie można odjąć tej ilości punktów. Teraz {log.points_log_class.class_number}{log.points_log_class.class_letter} klasa ma: {log.points_log_class.class_points}/1000 punktów. Nie może być mniej 0",
                    )
                else:
                    print(log.points_log_type)
                    log.points_log_class.class_points = (
                        log.points_log_class.class_points - log.points_log_amount
                    )
                    log.points_log_class.save()
                    log.save()
                    return HttpResponseRedirect("/")
    else:
        form = PointsLogCreateForm()

    return render(
        request,
        "create/create_points_log.html",
        {
            "form": form,
        },
    )


@login_required
def add_points_log(request, pk):
    points_log_class = get_object_or_404(Classes, pk=pk)
    if request.method == "POST":
        form = PointsAddSubtractLogCreateEditForm(request.POST)
        if form.is_valid():
            log = PointsLog(
                points_log_class=points_log_class,
                points_log_type=True,
                points_log_amount=form.cleaned_data["points_log_amount"],
                points_log_created_by=request.user,
            )
            check = log.points_log_class.class_points + log.points_log_amount
            if check > 1000:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"Nie można dodać tej ilości punktów. Teraz {points_log_class.class_number}{points_log_class.class_letter} klasa ma: {points_log_class.class_points}/1000 punktów.",
                )
            else:
                log.points_log_class.class_points = (
                    log.points_log_class.class_points + log.points_log_amount
                )
                log.points_log_class.save()
                log.save()
                return HttpResponseRedirect("/school/classes")
    else:
        form = PointsAddSubtractLogCreateEditForm()

    return render(
        request,
        "create/create_add_points_log.html",
        {"form": form, "classes": points_log_class},
    )


@login_required
def subtract_points_log(request, pk):
    points_log_class = get_object_or_404(Classes, pk=pk)
    if request.method == "POST":
        form = PointsAddSubtractLogCreateEditForm(request.POST)
        if form.is_valid():
            log = PointsLog(
                points_log_class=points_log_class,
                points_log_type=False,
                points_log_amount=form.cleaned_data["points_log_amount"],
                points_log_created_by=request.user,
            )
            check = log.points_log_class.class_points - log.points_log_amount
            if check < 0:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f"Nie można odjąć tej ilości punktów. Teraz {points_log_class.class_number}{points_log_class.class_letter} klasa ma: {points_log_class.class_points}/1000 punktów. Nie może być mniej 0",
                )
            else:
                log.points_log_class.class_points = (
                    log.points_log_class.class_points - log.points_log_amount
                )
                log.points_log_class.save()
                log.save()
                return HttpResponseRedirect("/school/classes")
    else:
        form = PointsAddSubtractLogCreateEditForm()

    return render(
        request,
        "create/create_subtract_points_log.html",
        {"form": form, "classes": points_log_class},
    )


@login_required
def delete_logs(request):
    if request.method == "POST":
        queryset = request.POST.getlist("logs")
        if queryset:
            PointsLog.objects.filter(id__in=queryset).delete()
        else:
            messages.add_message(
                request,
                messages.WARNING,
                "Rejestry do usunięcia nie są wybrane",
            )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class LogsList(LoginRequiredMixin, ListView):
    template_name = "logs.html"
    model = PointsLog
    context_object_name = "logs"
    ordering = ["-points_log_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PointsLogFilter(
            self.request.GET, self.get_queryset()
        )
        return context


class Scoreboard(ListView):
    template_name = "scoreboard.html"
    model = Classes
    context_object_name = "classes"

    ordering = ["-class_points"]


def scoreboard(request):
    all_classes = Classes.objects.all().order_by("-class_points")
    return render(
        request,
        "scoreboard.html",
        {
            "classes": all_classes,
        },
    )

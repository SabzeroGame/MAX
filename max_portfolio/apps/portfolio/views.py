"""Представления (views) для веб-интерфейса портфолио.

Задача файла: связать модели, формы и шаблоны для вывода страниц.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView

from .forms import ContactMessageForm, ProjectCreateForm
from .models import Category, Project, TeamMember


class HomeView(ListView):
    """Главная страница: список проектов + поиск, фильтры и визуальная статистика."""

    template_name = "portfolio/home.html"
    context_object_name = "projects"
    paginate_by = 6

    def get_queryset(self):
        # Базовый queryset: только опубликованные проекты.
        queryset = Project.objects.published().select_related("category", "created_by")

        # Получаем параметры фильтрации из query-string.
        q = self.request.GET.get("q", "").strip()
        category_slug = self.request.GET.get("category", "").strip()

        # Поиск по названию, краткому описанию и стеку.
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(tech_stack__icontains=q))

        # Фильтрация по категории.
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        # Дополняем контекст страницы статистикой и списком категорий.
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        context["selected_category"] = self.request.GET.get("category", "").strip()
        context["categories"] = Category.objects.annotate(total=Count("projects")).order_by("title")
        context["stats"] = {
            "projects": Project.objects.published().count(),
            "categories": Category.objects.count(),
            "members": TeamMember.objects.filter(is_active=True).count(),
        }
        context["featured_members"] = TeamMember.objects.filter(is_active=True)[:3]
        return context


class ProjectDetailView(DetailView):
    """Страница деталей конкретного проекта."""

    template_name = "portfolio/project_detail.html"
    model = Project
    context_object_name = "project"

    def get_object(self, queryset=None):
        # Берём проект по slug, включая автора и категорию одним SQL-запросом.
        return get_object_or_404(Project.all_objects.select_related("category", "created_by"), slug=self.kwargs["slug"])


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Создание проекта (только для авторизованных пользователей)."""

    template_name = "portfolio/project_form.html"
    form_class = ProjectCreateForm

    def form_valid(self, form):
        # Привязываем автора проекта к текущему пользователю.
        form.instance.created_by = self.request.user
        messages.success(self.request, _("Project was saved successfully."))
        return super().form_valid(form)


class AboutView(TemplateView):
    """Страница команды с активными участниками."""

    template_name = "portfolio/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = TeamMember.objects.filter(is_active=True)
        return context


class ContactView(FormView):
    """Страница обратной связи: сохранение входящего сообщения в БД."""

    template_name = "portfolio/contact.html"
    form_class = ContactMessageForm
    success_url = reverse_lazy("portfolio:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Thank you! Your message has been sent."))
        return super().form_valid(form)


class CategorySidebarView(TemplateView):
    """Вспомогательный блок категорий с кэшированием."""

    template_name = "includes/category_sidebar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = "portfolio_categories_with_counts"

        # Пытаемся взять данные из кэша.
        categories = cache.get(cache_key)
        if categories is None:
            # Если кэша нет — считаем и сохраняем на 60 секунд.
            categories = Category.objects.annotate(total=Count("projects")).order_by("title")
            cache.set(cache_key, categories, 60)

        context["categories"] = categories
        return context
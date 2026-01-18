from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


def csrf_failure(request, reason=''):
    """Кастомная страница ошибки 403 CSRF."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """Кастомная страница ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Кастомная страница ошибки 500."""
    return render(request, 'pages/500.html', status=500)


class AboutView(TemplateView):
    """Страница 'О проекте'."""
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Страница 'Правила'."""
    template_name = 'pages/rules.html'


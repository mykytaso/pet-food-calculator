from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView


class CalculatorView(TemplateView):
    template_name = "calculator/calculator.html"

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("This is the calculator view.")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["latest_articles"] = Article.objects.all()[:5]
    #     return context
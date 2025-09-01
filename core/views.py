from django.template.response import TemplateResponse


def home(request):
    return TemplateResponse(request, "core/index.html")


def show_privacy_policy(request):
    return TemplateResponse(request, "core/privacy_policy.html")


def show_terms_and_conditions(request):
    return TemplateResponse(request, "core/terms_conditions.html")

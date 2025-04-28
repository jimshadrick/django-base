from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "core/index.html"


class PrivacyPolicyView(TemplateView):
    template_name = "core/privacy_policy.html"


class TermsAndConditionsView(TemplateView):
    template_name = "core/terms_conditions.html"

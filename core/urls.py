from django.urls import path

from .views import home, show_privacy_policy, show_terms_and_conditions

app_name = 'core'

urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    path('', home, name='home'),
    path('privacy-policy/', show_privacy_policy, name="privacy_policy"),
    path('terms-and-conditions/', show_terms_and_conditions, name="terms_and_conditions")
]

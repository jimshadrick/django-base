from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Avoid circular import on startup
        from django.contrib.sites.models import Site

        # Update Site model on startup
        try:
            Site.objects.update_or_create(
                id=settings.SITE_ID,
                defaults={
                    'domain': settings.SITE_DOMAIN,
                    'name': settings.SITE_NAME,
                }
            )
        except Exception as e:
            # You can log this, but avoid crashing app on startup
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not update Site model on startup: {e}")

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialize or update the Django Site model based on settings'

    def handle(self, *args, **kwargs):
        site, created = Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': settings.SITE_DOMAIN,
                'name': settings.SITE_NAME,
            }
        )
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f'{action} site: {site.domain}'))

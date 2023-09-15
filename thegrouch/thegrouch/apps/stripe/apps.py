from django.urls import path

from oscar.core.application import OscarConfig


class StripeConfig(OscarConfig):
    name = 'thegrouch.apps.stripe'

    def ready(self):
        super().ready()
        from .views import WebhookView
        self.webhook_view = WebhookView

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('webhook/', self.webhook_view.as_view(), name='webhook'),
        ]
        return self.post_process_urls(urls)
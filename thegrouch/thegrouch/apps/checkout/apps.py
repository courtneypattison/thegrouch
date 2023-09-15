from django.urls import path

from oscar.apps.checkout.apps import CheckoutConfig as StripeCheckoutConfig


class CheckoutConfig(StripeCheckoutConfig):
    name = 'thegrouch.apps.checkout'

    def ready(self):
        super().ready()
        from .views import CancelView
        from oscar.apps.checkout.views import ThankYouView
        self.cancel_view = CancelView
        self.thank_you_view = ThankYouView

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('cancel/', self.cancel_view.as_view(), name='cancel'),
            path('thank-you/', self.thank_you_view.as_view(), name='thank_you'),
        ]
        return self.post_process_urls(urls)
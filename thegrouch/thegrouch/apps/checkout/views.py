import logging

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator

from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.payment.exceptions import RedirectRequired

from .facade import Facade

import stripe


logger = logging.getLogger('apps.checkout.views')

class PaymentDetailsView(OscarPaymentDetailsView):

    def handle_payment(self, order_number, total_incl_tax, **kwargs):
        url = Facade().get_redirect_url(order_number, total_incl_tax, self.request.user)
        raise RedirectRequired(url)

class CancelView(RedirectView):

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, "Transaction cancelled")
        return reverse('checkout:payment-details')
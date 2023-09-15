import logging

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from oscar.apps.checkout.views import OrderPlacementMixin
from oscar.apps.order.exceptions import UnableToPlaceOrder
from oscar.apps.payment.models import SourceType, Source
from oscar.core.loading import get_model

from .facade import Facade

Basket = get_model('basket', 'Basket')

logger = logging.getLogger('apps.stripe.views')

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(OrderPlacementMixin, View):
    """
    Handle Stripe checkout.session.completed event
    """
    def post(self, request):
        event = Facade().get_stripe_event(request)
        if event.type == 'checkout.session.completed':
            checkout = event.data.object

            order_number = checkout.client_reference_id
            order_total = checkout.amount_total

            user = self.request.user

            basket = Basket.objects.get(pk=self.checkout_session.get_submitted_basket_id())
            shipping_address = self.get_shipping_address(basket)
            shipping_charge = 0
            shipping_method = self.get_shipping_method(basket)
            billing_address = self.get_billing_address(shipping_address)

            source_type = SourceType.objects.get_or_create(name='stripe')
            source = Source(source_type=source_type,
                            currency=checkout.currency,
                            amount_allocated=order_total,
                            amount_debited=order_total)
            self.add_payment_source(source)
            self.add_payment_event('stripe', order_total, reference=checkout.id)

            try:
                self.handle_order_placement(order_number, user, basket, shipping_address, shipping_method,
                    shipping_charge, billing_address, order_total)
            except UnableToPlaceOrder as e:
                msg = str(e)
                logger.error("Order #%s: unable to place order - %s", order_number, msg, exc_info=True)
                self.restore_frozen_basket()
                return self.render_preview(self.request, error=msg)
            except Exception as e:

                logger.exception("Order #%s: unhandled exception while placing order (%s)", order_number, e)
                error_msg = "A problem occurred while placing this order. Please contact customer services."
                self.restore_frozen_basket()
                return self.render_preview(self.request, error=error_msg)


        return HttpResponse(status=200)
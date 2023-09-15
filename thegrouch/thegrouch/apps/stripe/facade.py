import json

from django.conf import settings

from oscar.apps.payment.exceptions import PaymentError

import stripe

class Facade(object):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
    
    def get_stripe_event(self, request):
        """
        Get Stripe event 
        """
        payload = request.body
        event = None
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Event.construct_from(
                json.loads(payload), sig_header, endpoint_secret, stripe.api_key
            )
        except ValueError as e:
            raise PaymentError("Invalid Payload")
        except stripe.error.SignatureVerificationError as e:
            raise PaymentError("Invalid Signature")

        return event

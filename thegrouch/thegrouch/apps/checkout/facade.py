import logging

from django.conf import settings

import stripe


logger = logging.getLogger('apps.checkout.facade')

# https://stripe.com/docs/currencies
ZERO_DECIMAL_CURRENCIES = (
    'BIF',
    'CLP',
    'DJF',
    'GNF',
    'JPY',
    'KMF',
    'KRW',
    'MGA',
    'PYG',
    'RWF',
    'VND',
    'VUV',
    'XAF',
    'XOF',
    'XPF',
)

THREE_DECIMAL_CURRENCIES = (
    'BHD',
    'JOD',
    'KWD',
    'OMR',
    'TND',
)

class Facade(object):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def get_redirect_url(self, order_number, total, user):
        """
        Return a URL for a Stripe checkout session
        """

        multiplier = 1
        if total.currency.upper() in ZERO_DECIMAL_CURRENCIES:
            multiplier = 1
        else:
            multiplier = 100
         
        amount = (total.incl_tax * multiplier).to_integral_value()
        if total.currency.upper() in THREE_DECIMAL_CURRENCIES:
            amount = round(amount, -1)

        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id = order_number,
                line_items = [{ 
                    "price_data": {
                        "unit_amount": amount,
                        "currency": total.currency.lower(), # Stripe API requires lowercase
                        'product_data': {
                            'name': 'The Grouch Products',
                            'description': 'Sewing and notions',
                        },
                    },
                    "quantity": 1,
                }],
                mode='payment',
                success_url=settings.SITE_URL + '/checkout/thank-you/',
                cancel_url=settings.SITE_URL + '/checkout/cancel/',
                customer_email=user.email,
            )
        except Exception as e:
            return str(e)
        return checkout_session.url
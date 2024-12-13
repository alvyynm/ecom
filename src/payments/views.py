from decimal import Decimal
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

import stripe

from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payments:completed'))
        cancel_url = request.build_absolute_uri(reverse('payments:canceled'))
        # create a stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )
        # create discount for stripe payment if order has a coupon applied
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.coupon.discount,
                duration='once'
            )
            # add discount to stripe checkout session
            session_data['discounts'] = [{'coupon': stripe_coupon}]
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payments/process.html', locals())


def payment_completed(request):
    return render(request, 'payments/completed.html')


def payment_canceled(request):
    return render(request, 'payments/canceled.html')

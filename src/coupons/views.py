from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon
# Create your views here.


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        coupon_code = form.cleaned_data['code']
        try:
            # check for valid coupon code
            coupon = Coupon.objects.get(code__iexact=coupon_code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            # store the coupon id in user session
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            # if it doesn't exist, store None
            request.session['coupon_id'] = None
        return redirect('cart:cart_detail')

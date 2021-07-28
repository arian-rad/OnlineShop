from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm


class CouponApplyView(View):
    def post(self, request):
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                # Using iexact field lookup to perform a case-insensitive exact match.
                coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=timezone.now(),
                                            valid_to__gte=timezone.now(), active=True)
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
        return redirect('cart:cart_detail')



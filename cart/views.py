from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.views.generic import TemplateView, View


class CartAdd(View):
    # @require_POST Why do I get an error for this?
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('cart:cart_detail')


class CartRemove(View):
    # @require_POST 'CartRemove' object has no attribute 'method'
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(TemplateView):  # Didn't inherit from DetailView because there is no model for cart!
    template_name = 'cart/cart_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(CartDetailView, self).get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        for item in context['cart']:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})

        return context



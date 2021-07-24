from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View


class CartAdd(View):
    @require_POST
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product, quantity=cd['quantity'], override_quantity=cd['override_quantity'])
        return redirect('cart:cart_detail')


class CartRemove(View):
    @require_POST
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

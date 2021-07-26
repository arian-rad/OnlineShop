from django.shortcuts import render
from django.views.generic import View
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart
from orders.tasks import order_created


class OrderCreateView(View):  # Didn't use CreateView because I was facing multiple models: OrderItem, Order
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, 'orders/order_create_view.html', {'cart': cart, 'form': form})

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)  # launching asynchronous task
            return render(request, 'orders/success.html', {'order': order})

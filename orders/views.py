from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView, TemplateView
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm
from cart.cart import Cart
import zarinpal
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


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
            # order_created.delay(order.id) Moved this line to zarinpal\views.py
            # because email must be sent after payment verification
            request.session['order_id'] = order.id
            zarinpal.views.amount = order.get_total_cost()
            return redirect('zarinpal:request')


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetailView(TemplateView):
    template_name = 'orders/admin/order_admin_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(AdminOrderDetailView, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=self.kwargs['order_id'])
        return context


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderPDFView(View):
    """
    This is the view to generate a PDF invoice for an order.
    """

    def get(self, request, order_id):
        # context = super(AdminOrderPDFView, self).get_context_data(**kwargs)
        order = get_object_or_404(Order, id=order_id)
        html = render_to_string('orders/pdf.html', {'order': order})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
        # print('STATICFILES_DIRS:', settings.STATICFILES_DIRS[0])
        # print('STATIC_ROOT:', settings.STATIC_ROOT)
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(str(settings.STATICFILES_DIRS[0]) + '/' + 'css/pdf.css')])
        # weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS((settings.STATIC_ROOT) + 'css/pdf.css')])
        return response

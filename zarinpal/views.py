from django.http import HttpResponse
from django.shortcuts import redirect, render
from zeep import Client
from orders.models import Order
from orders.tasks import order_created
from .tasks import payment_completed

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات خرید شما"  # Required
email = 'email@example.com'  # Optional
mobile = ''  # Optional
CallbackURL = 'http://127.0.0.1:8000/payment/verify/'  # Important: need to edit for realy server.


def send_request(request):
    client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
    order = Order.objects.get(id=request.session.get('order_id'))
    amount = order.get_total_cost()
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        order = Order.objects.get(id=request.session.get('order_id'))
        if result.Status == 100:
            order.paid = True
            order.save()
            # order_created.delay(order.id)  # launching asynchronous task
            payment_completed.delay(order.id)  # launching asynchronous task: Sending an email
            return render(request, 'orders/success.html', {'order': order})
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            order_created.delay(order.id)  # launching asynchronous task
            return render(request, 'orders/fail.html')
    else:
        return render(request, 'orders/fail.html')

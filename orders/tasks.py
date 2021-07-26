from celery import task
from django.core.mail import send_mail
from orders.models import Order


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is    successfully created.
    """
    order = Order.objects.get(id=order_id)
    email_subject = f'Order nr. {order.id}'
    email_message = f'Dear {order.first_name},\n\n' \
                    f'You have successfully placed an order.' \
                    f'Your order ID is {order.id}.'
    mail_sent = send_mail(email_subject, email_message, 'admin@myshop.com', [order.email])

    return mail_sent

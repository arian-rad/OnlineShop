from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


"""
Django’s send_mail() and send_mass_mail() functions are actually thin wrappers 
that make use of the EmailMessage class.
Not all features of the EmailMessage class are available 
through the send_mail() and related wrapper functions.
If you wish to use advanced features,
such as BCC’ed recipients, file attachments, or multi-part email,
you’ll need to create EmailMessage instances directly.
"""


@task
def payment_completed(order_id):
    """
     Task to send an e-mail notification when an order is  successfully created.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    email_subject = f'My Shop - EE Invoice no. {order.id}'
    email_message = f'Hi {order.first_name} {order.last_name}, Thank you for shopping.\n\n' \
                    f'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(email_subject, email_message, 'admin@myshop.com', [order.email])

    # generate PDF
    html = render_to_string('orders/pdf.html', {'order': order})
    out = BytesIO()
    # stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    stylesheets = [weasyprint.CSS(str(settings.STATICFILES_DIRS[0]) + '/' + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach the generated PDF file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # send mail
    email.send()

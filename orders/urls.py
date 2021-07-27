from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('admin/order/<int:order_id>/', views.AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.AdminOrderPDFView.as_view(), name='admin_order_pdf'),
]

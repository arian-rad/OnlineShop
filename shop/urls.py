from django.urls import path
from shop.views import ProductListView, ProductDetailView


app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),  # adding this in case no category was selected
    path('<str:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
]

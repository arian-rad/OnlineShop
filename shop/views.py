from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from shop.models import Product, Category
from cart.forms import CartAddProductForm
from parler.views import TranslatableSlugMixin


class ProductListView(ListView):
    """
    A class to View available products based on a category(optional)
    """
    model = Product
    template_name = 'shop/product_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category = None
        context['categories'] = Category.objects.all()  # we only want to view available products
        products = Product.objects.filter(available=True)
        if 'category_slug' in self.kwargs.keys():
            language = self.request.LANGUAGE_CODE
            category = get_object_or_404(Category, translations__slug=self.kwargs['category_slug'],
                                         translations__language_code=language)
            products = products.filter(category=category)
        context['category'] = category
        context['products'] = products
        return context


class ProductDetailView(TranslatableSlugMixin, DetailView):
    model = Product
    template_name = 'shop/product_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        language = self.request.LANGUAGE_CODE
        context['product'] = get_object_or_404(
            Product, id=self.kwargs['id'], translations__slug=self.kwargs['slug'],
            translations__language_code=language, available=True)

        context['cart_product_form'] = CartAddProductForm()
        return context


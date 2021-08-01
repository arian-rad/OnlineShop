from django.shortcuts import render,  get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from shop.models import Product, Category
from cart.forms import CartAddProductForm
from parler.views import TranslatableSlugMixin


class ProductListView(ListView):
    """
    A class to View available products based on a category(optional)
    """
    model = Product
    template_name = 'shop/product_list_view.html'
    # slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category = None
        context['categories'] = Category.objects.all()  # we only want to view available products
        products = Product.objects.filter(available=True)
        if 'category_slug' in self.kwargs.keys():
            category = get_object_or_404(Category, translations__slug=self.kwargs['category_slug'])
            products = products.filter(category=category)
        context['category'] = category
        context['products'] = products
        return context


class ProductDetailView(TranslatableSlugMixin, DetailView):
    model = Product
    template_name = 'shop/product_detail_view.html'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        print(self.kwargs)
        context['product'] = get_object_or_404(Product, id=self.kwargs['id'], translations__slug=self.kwargs['product_slug'], available=True)
        context['cart_product_form'] = CartAddProductForm()
        return context


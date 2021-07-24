from django.shortcuts import render,  get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from shop.models import Product, Category
from cart.forms import CartAddProductForm


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
            category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            products = products.filter(category=category)
        context['category'] = category
        context['products'] = products
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, id=self.kwargs['id'], slug=self.kwargs['slug'],  available=True)
        context['cart_product_form'] = CartAddProductForm()
        return context


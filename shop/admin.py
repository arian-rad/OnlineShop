from django.contrib import admin
from shop.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available', 'created', 'updated')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'available')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

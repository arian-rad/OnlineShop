from django.db import models
from django.utils.text import slugify  # Not mentioned in Creating product catalog models task
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('name'), max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def save(self, **kwargs):  # Not mentioned in Creating product catalog models task
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(**kwargs)


class Product(models.Model):
    name = models.CharField(_('name'), max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name=_('category'))
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, **kwargs):  # Not mentioned in Creating product catalog models task
        self.slug = slugify(self.name, allow_unicode=True)
        super(Product, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

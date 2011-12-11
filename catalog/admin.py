# coding:utf8
from avrora.catalog.models import Product, Manufacturer
from avrora.catalog.models import Category
from django.contrib import admin


def make_active_product(modeladmin, request, queryset):
    queryset.update(active=True)
make_active_product.short_description =u'Установить Active'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'active','sku' ,'price')
    search_fields = ['name']
    prepopulated_fields = {'slug' : ('name',)}
    actions = [make_active_product]
    

    

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    prepopulated_fields = {'slug' : ('name',)}
    
admin.site.register(Manufacturer)
admin.site.register(Category, CategoryAdmin)
from django.contrib import admin

from .models import Product, Company, CompanyProduct, Category


class CompanyInLine(admin.TabularInline):
    model = CompanyProduct
    rows = 4


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name', 'category',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    serch_fields = ('name', 'owner',)
    list_filter = ('foundation_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

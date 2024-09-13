from django.contrib import admin

from .models import Product, Company, CompanyProduct, Category, CategoryProduct


class CategoryInLine(admin.TabularInline):
    model = CategoryProduct
    rows = 4


class CompanyInLine(admin.TabularInline):
    model = CompanyProduct
    rows = 4


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name',)
    list_filter = ('name', 'price', 'category',)
    inlines = (CategoryInLine,)


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

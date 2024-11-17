from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet, CompanyViewSet,
    CategoryViewSet, ProductViewSet,
    ItemViewSet, CartViewSet,
)


router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('companies', CompanyViewSet, basename='companies')
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')
router.register('shopping-cart', CartViewSet, basename='shopping-cart')
router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet, CompanyViewSet,
    CategoryViewSet, ProductViewSet,
    ShoppingCartView,
    get_shopping_cart
)


router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('companies', CompanyViewSet, basename='companies')
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'products/<int:id>/shopping-cart/',
        ShoppingCartView.as_view(),
        name='shopping-cart'

    ),
    path('shopping-cart/', get_shopping_cart, name='get_shopping_cart')
]

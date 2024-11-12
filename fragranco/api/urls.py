from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet, CompanyViewSet,
    CategoryViewSet, ProductViewSet
)


router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('companies', CompanyViewSet, basename='companies')
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]

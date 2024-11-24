from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet, CompanyViewSet,
    CategoryViewSet, ProductViewSet,
    ItemView, ListItemView,
)


router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('companies', CompanyViewSet, basename='companies')
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:id>/add-item/', ItemView.as_view(), name='add_item'),
    path('cart/', ListItemView.as_view(), name='cart'),
]

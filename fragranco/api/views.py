from rest_framework import views, viewsets
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response
from djoser.views import UserViewSet

from users.models import CustomUser
from products.models import (
    Company, Category,
    Product, ShoppingCart,
)
from .serializers import (
    CustomUserSerializer, CompanySerializer,
    CategorySerializer, ListProductSerializer,
    CreateProductSerializer,
    RetrieveProductSerializer,
    ShoppingCartSerializer,
)
from .mixins import PostDeleteMixin


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProductSerializer
        if self.action == 'retrieve':
            return RetrieveProductSerializer
        return ListProductSerializer

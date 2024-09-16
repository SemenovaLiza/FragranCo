from rest_framework import views, viewsets
from djoser.views import UserViewSet

from users.models import CustomUser
from products.models import (
    Company, Category,
    Product,
)
from .serializers import (
    CustomUserSerializer, CompanySerializer,
    CategorySerializer, ProductSerializer,
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartView(PostDeleteMixin, views.APIView):
    obj_to_add_model = Product
    serializer_class = ShoppingCartSerializer

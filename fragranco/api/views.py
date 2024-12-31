from rest_framework import views, viewsets, generics
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from users.models import CustomUser
from products.models import (
    Company, Category,
    Product, Item, Review,
)
from .serializers import (
    CustomUserSerializer, CompanySerializer,
    ListProductSerializer,
    CreateProductSerializer,
    RetrieveProductSerializer,
    ItemSerializer,
    ListItemSerializer,
    CategorySerializer,
    ReviewSerializer,
    ListReviewSerializer,
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

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProductSerializer
        if self.action == 'retrieve':
            return RetrieveProductSerializer
        return ListProductSerializer


class ItemView(PostDeleteMixin, views.APIView):
    model = Item
    obj_to_add_model = Product
    serializer_class = ItemSerializer
    object_to_add_name = 'product'


class ListItemView(ListModelMixin, GenericAPIView):
    def get(self, request):
        user = CustomUser.objects.filter(id=request.user.id)
        serializer = ListItemSerializer(user, many=True)
        return Response(serializer.data)


class ReviewCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListReviewSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        print(self.request)


class ReviewDelete(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ListReviewSerializer

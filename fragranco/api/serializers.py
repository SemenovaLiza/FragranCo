from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from users.models import CustomUser
from products.models import (
    Company, CompanyProduct, Category,
    Product, Item, Cart
)


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)

    def validate(self, data):
        if data['email'] == data['password']:
            raise serializers.ValidationError(
                "Email should't be used as password!"
            )
        elif data['username'] == data['email']:
            raise serializers.ValidationError(
                "Username shouldn't be you email!"
            )
        return data


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Company
        fields = ('name', 'owner', 'foundation_date',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'temporarity',)


class CompanyProductSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        write_only=True
    )
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = CompanyProduct
        fields = ('id', 'company_name', 'price')  # add amount of product left


class RetrieveProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    sellers = CompanyProductSerializer(many=True, source='companies_in_product')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'sellers', 'category')


class ListProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price')

    def get_price(self, obj):
        prices = []
        for i in CompanyProduct.objects.filter(product=obj.id):
            prices.append(i.price)
        return min(prices)


class ShortProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', )


class CreateProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    sellers = CompanyProductSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'sellers', 'category',)
        depth = 1

    def create(self, validated_data):
        categories = validated_data.pop('category')
        sellers = validated_data.pop('sellers')
        product = Product.objects.create(**validated_data)
        for seller in sellers:
            CompanyProduct.objects.create(product=product, company=seller['id'], price=seller['price'])
        product.category.add(*categories)
        return product

    def to_representation(self, instance):
        return ListProductSerializer(
            instance
        ).data


class BigCart(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    items = ListProductSerializer(read_only=True, many=True)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'item',)


class ItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('product',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'user', 'product',)


class ListItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('id', 'user', 'items',)

    def get_items(self, obj):
        items = Item.objects.filter(user=obj.user.id)
        return ItemSerializer(items, many=True).data

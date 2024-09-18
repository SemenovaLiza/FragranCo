from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from users.models import CustomUser
from products.models import Company, Category, Product, ShoppingCart, ShoppingCartItem, CategoryProduct


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
    class Meta:
        model = Company
        fields = ('name', 'owner', 'foundation_date',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'temporarity',)


class CategoryProductSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = CategoryProduct
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'sellers', 'category',)

    
    def create(self, validated_data):
        categories = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        for category in categories:
            current_category, status = Category.objects.get_or_create(**category)
            CategoryProduct.objects.create(product=product, category=current_category)

        return product


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product')

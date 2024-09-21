from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from users.models import CustomUser
from products.models import Company, Category, Product, ShoppingCart, ShoppingCartItem


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
        fields = ('id', 'name', 'temporarity',)


class ListProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'sellers', 'category')

        # def get_category(self, obj):
        #     return CategoryProductSerializer(categories, many=True).data


class CreateProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'description', 'sellers', 'category',)
        depth = 1

    def create(self, validated_data):
        categories = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.add(*categories)
        return product

    def to_representation(self, instance):
        return ListProductSerializer(
            instance
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product')

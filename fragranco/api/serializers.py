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
        fields = ('id', 'name', 'temporarity',)


class CategoryProductSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = CategoryProduct
        fields = ('id', 'name',)


class ListProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(many=True, source='companies_in_product')

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'sellers', 'category')

        def get_category(self, obj):
            categories = CategoryProduct.objects.filter(product=obj.id)
            print(obj.id)
            print(categories)
            return CategoryProductSerializer(categories, many=True).data


class CategoryProductSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = CategoryProduct
        fields = ('id', 'name',)


class CreateProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'sellers', 'category',)

    def create(self, validated_data):
        categories = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        for category in categories:
            CategoryProduct.objects.create(product=product, category=category.pop('id'))
            cat = CategoryProduct.objects.filter(product=product.id)
        product.category.set(categories)
        return product

    #def to_representation(self, value):


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product')

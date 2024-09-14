from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from users.models import CustomUser
from products.models import Company, Category, Product


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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'sellers', 'category',)

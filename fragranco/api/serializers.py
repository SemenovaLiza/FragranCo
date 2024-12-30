import base64
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.core.files.base import ContentFile

from users.models import CustomUser
from products.models import (
    Company, CompanyProduct, Category,
    Product, Item, Review,
)


# data:image/png;base64,'<data>'
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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
    number_of_products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'temporarity', 'number_of_products',)

    def get_number_of_products(self, obj):
        return Product.objects.filter(category=obj).count()


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
    sellers = CompanyProductSerializer(
        many=True, source='companies_in_product')

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
        fields = ('id', 'name',)


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
            CompanyProduct.objects.create(
                product=product, company=seller['id'], price=seller['price']
            )
        product.category.add(*categories)
        return product

    def to_representation(self, instance):
        return ListProductSerializer(
            instance
        ).data


class ItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'product', 'amount',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'user', 'product', 'amount',)

    def create(self, validated_data):
        if Item.objects.filter(
            user=validated_data['user'], product=validated_data['product']
        ).exists():
            item = Item.objects.get(
                user=validated_data['user'], product=validated_data['product']
            )
            item.amount += 1
            item.save()
            return item
        return super().create(validated_data)


class ListItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'items',)

    def get_items(self, obj):
        items = Item.objects.filter(user=obj.id)
        return ItemShortSerializer(items, many=True).data


class ReviewSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'image',)

    def create(self, validated_data):
        product_id = self.context['request'].parser_context['kwargs']['id']
        product = Product.objects.get(id=product_id)
        user = self.context['request'].user
        review = Review.objects.create(**validated_data, product=product, user=user)
        return review


class ListReviewSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    product = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'product', 'user', 'text', 'rating', 'image',)

    def get_product(self, obj):
        data = {
            'id': obj.product.id,
            'name': obj.product.name,
        }
        return data

    def get_user(self, obj):
        data = {
            'id': obj.user.id,
            'username': obj.user.username,
        }
        return data

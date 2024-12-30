from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import CustomUser


# unique name
class Company(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Owner'
    )
    foundation_date = models.DateField()

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Category(models.Model):
    name = models.CharField(max_length=64)
    temporarity = models.BooleanField(verbose_name='Is category temporary')
    # If category was created for certain event like Christmas or Helloween
    # it will be marked like "temporary category".

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# change sellers to seller
class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    sellers = models.ManyToManyField(
        Company,
        through='CompanyProduct',
        verbose_name='Companies'
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='Categories'
    )
    # positive small integer's biggest number is 32767.
    # However, product can cost more that 33000.

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class CompanyProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='companies_in_product',
        verbose_name='Product',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Company'
    )
    price = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return self.company.name, self.price


class Item(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='shopping cart'
    )
    product = models.ForeignKey(
        Product,
        related_name='product_in_carts_item', #чтобы высчитать популярность продукта  добавить поле со стаутсом купила/нет и так проверять попоулярность продукта
        on_delete=models.CASCADE,
        verbose_name='products in carts item'
    )
    amount = models.PositiveSmallIntegerField(default=1)


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='review author'
    )
    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='product'
    )
    created_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    photo = models.ImageField(upload_to='reviews/images/', null=True, default=None)
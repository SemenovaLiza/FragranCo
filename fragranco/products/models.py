from django.db import models
from django.core.validators import MinValueValidator

from users.models import CustomUser


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

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# change sellers to seller
class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sellers = models.ManyToManyField(
        Company,
        through='CompanyProduct',
        verbose_name='Companies'
    )
    category = models.ManyToManyField(
        Category,
        through='CategoryProduct',
        verbose_name='Categories'
    )
    # positive small integer's biggest number is 32767.
    # However, product can cost more that 33000.

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class CategoryProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='categories_in_product',
        verbose_name='Product'
    )
    # cascad because if this product is deleted ->
    # relation between it and certain category will be deleted as well.
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Category'
    )


class CompanyProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='companies_in_product',
        verbose_name='Product'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Company'
    )

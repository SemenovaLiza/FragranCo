from django.db.models.signals import pre_save
from django.dispatch import receiver
from products.models import Item


@receiver(pre_save, sender=Item)
def increase_item_amount(sender, instance, **kwargs):
    try:
        item = Item.objects.get(user=instance.user, product=instance.product)
        instance.amount = item.amount + 1
        item.save()
        instance.pk = None
    except Item.DoesNotExist:
        pass


#{
#    "username": "lizon",
#    "email": "liza@gmail.com",
#    "password": "d14hgpokidoki"
#}
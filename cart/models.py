from decimal import Decimal

from django.db import models

from coupons.models import Coupon
from products.models import Product
from users.models import User


class Session(models.Model):
    """
    The model for saving the session key is needed so that after the user pays for the order,
     reset the value of the coupon in the session.
    """
    session_key = models.CharField(max_length=128)
    payment_id = models.CharField(max_length=128)


class CartQuerySet(models.QuerySet):

    def get_total_price_after_discount(self):
        """Returns the discounted price."""
        return self.total_sum() - self.get_discount()

    def get_discount(self):
        """Returns the amount of the discount."""
        coupons = [cart.coupon for cart in self if isinstance(cart.coupon, Coupon)]
        if coupons:
            coupon = Coupon.objects.get(code=coupons[0].code)
            if coupon.active:
                return (coupon.discount / Decimal('100')) * self.total_sum()
        return Decimal('0')

    def total_sum(self):
        """Returns the sum of all carts."""
        return sum([cart.sum() for cart in self])

    def total_quantity(self):
        """Returns the quantity of all carts."""
        return sum([cart.quantity for cart in self])


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(to=Coupon, on_delete=models.CASCADE, blank=True, null=True)

    objects = CartQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        """Returns the amount of the cart."""
        return self.product.price * self.quantity

    @classmethod
    def create_or_update(cls, product_id, user, quantity, coupon_code):
        """
        Creates a user's shopping cart and adds a product to it. If the product is in the cart, it updates its quantity.
        """

        cart = Cart.objects.filter(user=user, product_id=product_id)
        if coupon_code is not None:
            coupon = Coupon.objects.get(code=coupon_code)
        else:
            coupon = None

        if not cart.exists():
            if coupon is not None:
                obj = Cart.objects.create(user=user, product_id=product_id, quantity=quantity, coupon=coupon)
            else:
                obj = Cart.objects.create(user=user, product_id=product_id, quantity=quantity)
            is_created = True
            return obj, is_created
        else:
            cart = cart.first()
            cart.quantity += 1
            cart.save()
            is_created = False
            return cart, is_created

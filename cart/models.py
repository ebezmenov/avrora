from django.db import models
from django.contrib.auth.models import User
from avrora.catalog.models import Product

class Cart(models.Model):
    """A cart is a container for products which are supposed to be bought by a
    shop customer.

    Instance variables:

    - user
       The user to which the cart belongs to
    - session
       The session to which the cart belongs to

    A cart can be assigned either to the current logged in User (in case
    the shop user is logged in) or to the current session (in case the shop user
    is not logged in).

    A cart is only created if it needs to. When the shop user adds something to
    the cart.
    """
    user = models.ForeignKey(User, verbose_name=(u"User"), blank=True, null=True)
    creation_date = models.DateTimeField((u"Creation date"), auto_now_add=True)
    modification_date = models.DateTimeField((u"Modification date"), auto_now=True, auto_now_add=True)
    
class CartItem(models.Model):
    """A cart item belongs to a cart. It stores the product and the amount of
    the product which has been taken into the cart.

    Instance variables:

    - product
       A reference to a product which is supposed to be bought
    - amount
       Amount of the product which is supposed to be bought.
    """
    cart = models.ForeignKey(Cart, verbose_name=(u"Cart"))
    product = models.ForeignKey(Product, verbose_name=(u"Product"))
    amount = models.FloatField((u"Quantity"), blank=True, null=True)
    creation_date = models.DateTimeField((u"Creation date"), auto_now_add=True)
    modification_date = models.DateTimeField((u"Modification date"), auto_now=True, auto_now_add=True)


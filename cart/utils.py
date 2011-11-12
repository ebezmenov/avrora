from django.core.exceptions import ObjectDoesNotExist
from avrora.cart.models import Cart

def get_cart(request):
    """Returns the cart of the current customer or None.
    """
    user = request.user
    try:
        cart = Cart.objects.get(user = user)
        return cart
    except ObjectDoesNotExist:
            return None
  
def create_cart(request):
    """Creates a cart for the current session and/or user.
    """
    cart = Cart(user = request.user)
    cart.save()
    return cart

def get_or_create_cart(request):
    """Returns the cart of the current user. If no cart exists it creates a new
    one first.
    """
    cart = get_cart(request)
    if cart is None:
        cart = create_cart(request)

    return cart

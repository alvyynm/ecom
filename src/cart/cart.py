from decimal import Decimal
from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        """Initialize the cart instance

        Args:
            request (_type_): _description_
        """
        # store the current session to self.session
        self.session = request.session

        # get the cart instance from session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # if cart doesn't exist, create an empty cart and save to session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

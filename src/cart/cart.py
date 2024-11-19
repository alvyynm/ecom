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

    def __iter__(self):
        """
            Iterate over the items in the cart and get the products
            from the database.
            """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Counts the number of items in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update quantity

        Args:
            product (Product): Product to add
            quantity (int, optional): Quantity of the product. Defaults to 1.
            override_quantity (bool, optional): Override quantity of product in cart. Defaults to False.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # mark the session as modified to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """Remove given product from the cart dictionary"""
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """Calculates the total price of the items in the cart"""
        return sum(
            Decimal(item['price'] * item['quantity'])
            for item in self.cart.values()
        )

    def clear(self):
        """Clears the cart"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        cart.add(
            product=product,
            quantity=data['quantity'],
            override_quantity=data['override'],
        )
    return redirect('cart:cart_detail')

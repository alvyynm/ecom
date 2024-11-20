from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


def order_create(request):
    # obtain the current cart from the session
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            # create a new order in the db
            order = form.save()

            for item in cart:
                # create a new order item for each cart item
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            # clear the cart after order is created
            cart.clear()

            # launch asychronous created_order task
            order_created.delay(order.id)

            return render(
                request,
                'orders/order/created.html',
                {'order': order}
            )
    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html', {
                      'cart': cart, 'form': form
                  })

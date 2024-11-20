from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
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
            # add order id to session
            request.session['order_id'] = order.id
            # redirect to payment page
            return redirect('payments:process')
    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html', {
                      'cart': cart, 'form': form
                  })


@staff_member_required
def admin_order_detail(request, order_id):
    """Custom admin view for order detail"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

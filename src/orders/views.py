import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.staticfiles import finders
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    # obtain the current cart from the session
    cart = Cart(request)

    if request.user.is_authenticated:
        # if the user is authenticated
        # no form to create an order is displayed
        order_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': request.user.profile.delivery_address,
            'postal_code': request.user.profile.postal_code,
            'city': request.user.profile.city,
            'user': request.user
        }

        if request.method == 'POST':
            if cart.coupon:
                order_data.coupon = cart.coupon
                order_data.discount = cart.coupon.discount

            # print(order_data)
            # create a new order directly with the order data
            order = Order.objects.create(**order_data)

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
            messages.success(
                request, 'Order has been placed, continue to payment page.')
            # redirect to payment page
            return redirect('payments:process')
            # if the form is invalid
        return render(request, 'orders/order/create.html', {'cart': cart})
    else:
        # if the user is not logged in
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)

            if form.is_valid():
                # create a new order instance and don't save it
                order = form.save(commit=False)

                if cart.coupon:
                    order.coupon = cart.coupon
                    order.discount = cart.coupon.discount

                # save the order
                order.save()
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


@staff_member_required
def admin_order_pdf(request, order_id):
    """Generate pdf invoice for a given order"""
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))],
    )
    return response


@login_required
def order_list(request):
    """Displays the user's order list"""
    user = request.user

    orders = user.orders.all()

    return render(request, 'orders/order/list.html', {'orders': orders})


@login_required
@require_POST
def order_cancel(request, order_id):
    """Cancel an un-paid order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.canceled:
        messages.warning(request, "Order has already been canceled")
    else:
        order.cancel()
        messages.success(request, "Order canceled successfully")

    return redirect('orders:order_list')


def order_detail(request, order_id):
    """View a single order's details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'orders/order/detail.html', {'order': order})


def print_order(request, order_id):
    """Let a user generate pdf invoice for a given order"""
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))],
    )
    return response

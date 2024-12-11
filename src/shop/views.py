from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Category, Product, Tag
from cart.forms import CartAddProductForm
from .recommender import Recommender

# Create your views here.


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_slug:
        # if the category slug is provided, filter by category
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    sort_by = request.GET.get('sort_by')
    sorting_fields = ['price', '-price',
                      '-created', '-discount_percentage']

    if sort_by in sorting_fields:
        products = products.order_by(sort_by)

    # paginate products
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 10)  # return 10 products per page
    page_obj = paginator.get_page(page_number)

    # if the request is from htmx, render the partial
    if request.htmx:
        return render(request, 'shop/product/partials/product_list.html', {
            'products': page_obj.object_list,
            'page_obj': page_obj
        })

    # render the full page for non-htmx requests
    return render(request,
                  'shop/product/list.html',
                  {
                      'category': category,
                      'products': page_obj.object_list,
                      'page_obj': page_obj
                  })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # display add to cart button
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request, 'shop/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})


def gift_ideas(request):
    gift_query = Tag.objects.get(name='gift ideas')
    for_her_query = Tag.objects.get(name='For Her')
    for_him_query = Tag.objects.get(name='For Him')
    under_50_query = Tag.objects.get(name='Under 50')
    gifts = gift_query.products.filter(available=True)
    gifts_for_her = for_her_query.products.filter(available=True)
    gifts_for_him = for_him_query.products.filter(available=True)
    gifts_under_50 = under_50_query.products.filter(available=True)

    sort_by = request.GET.get('sort_by')
    sorting_fields = ['price', '-price',
                      '-created', '-discount_percentage']

    if sort_by in sorting_fields:
        gifts = gifts.order_by(sort_by)

    return render(request, 'shop/product/gift_ideas.html', {
        'gifts': gifts,
        'gifts_for_her': gifts_for_her,
        'gifts_for_him': gifts_for_him,
        'gifts_under_50': gifts_under_50
    })


def todays_deals(request):
    """View for displaying Today's Deals"""
    todays_deals_query = Tag.objects.get(slug='todays-deals')
    under_50_query = Tag.objects.get(slug='under-50')
    deals_under_50 = under_50_query.products.filter(available=True)
    todays_deals = todays_deals_query.products.filter(available=True)

    sort_by = request.GET.get('sort_by')
    sorting_fields = ['price', '-price',
                      '-created', '-discount_percentage']

    if sort_by in sorting_fields:
        todays_deals = todays_deals.order_by(sort_by)

    return render(request, 'shop/product/deals.html', {
        'deals': todays_deals,
        'under_50': deals_under_50
    })

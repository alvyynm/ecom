from .models import Category


def all_categories(request):
    """Returns all categories"""
    categories = Category.objects.all()

    return {
        'categories': categories
    }

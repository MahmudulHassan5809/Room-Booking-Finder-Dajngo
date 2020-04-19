from .models import Category


def categories(request):
    all_cats = Category.objects.all()
    return {'all_categories': all_cats}

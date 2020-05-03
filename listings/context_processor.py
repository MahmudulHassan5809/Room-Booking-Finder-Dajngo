from .models import Category, Listing


def categories(request):
    all_cats = Category.objects.all()
    return {'all_categories': all_cats}


def common_tags(request):
    common_tags = Listing.tags.most_common()[:4]
    return {'common_tags': common_tags}


def cities(request):
    all_city = Listing.objects.order_by(
        'city').values_list('city', flat=True).distinct()
    return {'all_city': all_city}


def areas(request):
    all_area = Listing.objects.order_by(
        'area').values_list('area', flat=True).distinct()
    return {'all_area': all_area}

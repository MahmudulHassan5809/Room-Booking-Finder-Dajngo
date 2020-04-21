from .models import Category, Listing


def categories(request):
    all_cats = Category.objects.all()
    return {'all_categories': all_cats}


def common_tags(request):
    common_tags = Listing.tags.most_common()[:4]
    return {'common_tags': common_tags}

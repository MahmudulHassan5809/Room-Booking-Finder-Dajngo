from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Category, Listing, ListingImage, ListingExtra, ListingRating, ListingComment


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "image"]
    search_fields = ('name', 'slug',)
    list_filter = ['name']
    exclude = ['slug']
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)


class ListingImageInline(admin.StackedInline):
    model = ListingImage
    extra = 0


class ListingExtraInline(admin.StackedInline):
    model = ListingExtra
    extra = 0


class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline, ListingExtraInline]

    list_display = ["title", "category",
                    "status", "price", "active", "booked", "tag_list", "end_time"]
    search_fields = ('title', 'slug', 'category__name',
                     'status', 'active', 'tags__name')
    list_filter = ['category__name', 'status', 'active', 'booked']
    list_editable = ['active']
    exclude = ['slug']
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.listing_images.create(image=afile)


admin.site.register(Listing, ListingAdmin)


class ListingRatingAdmin(admin.ModelAdmin):
    list_display = ["listing", "user", "average_rating"]
    search_fields = ['listing__title', 'user__username']
    autocomplete_fields = ['listing', 'user']


admin.site.register(ListingRating, ListingRatingAdmin)


class ListingCommentAdmin(admin.ModelAdmin):
    list_display = ["listing", "user"]
    search_fields = ['listing__title', 'user__username']
    autocomplete_fields = ['listing', 'user']


admin.site.register(ListingComment, ListingCommentAdmin)

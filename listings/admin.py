from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Category, Listing, ListingImage


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


class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]

    list_display = ["title", "category",
                    "status", "price", "active", "end_time"]
    search_fields = ('title', 'slug', 'category__name',
                     'status', 'active')
    list_filter = ['category__name', 'status', 'active']
    list_editable = ['active']
    exclude = ['slug']
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.listing_images.create(image=afile)


admin.site.register(Listing, ListingAdmin)

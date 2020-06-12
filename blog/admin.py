from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from .models import Article

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50px"/>'.format(obj.image.url))

    image_tag.short_description = 'Article Image'

    list_display = ["title", "image_tag", "author", "short_description","active"]
    search_fields = ('title', 'content',)
    list_filter = ['author__username']
    list_editable = ['active']
    #autocomplete_fields = ['author']
    list_per_page = 20

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = get_user_model().objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Article, ArticleAdmin)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing, Category
from django.views import generic
from django.views import View

# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        conext = {
            'title': 'Home'
        }
        return render(request, 'listings/home.html', conext)


class CategoryRooms(generic.ListView):
    model = Listing
    context_object_name = 'liting_list'
    paginate_by = 10
    template_name = 'listings/liting_list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category_obj = get_object_or_404(Category, slug=category_slug)

        liting_list = Listing.active_objects.filter(category=category_obj)
        return liting_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        context['title'] = f'{category_slug} Listings'
        return context

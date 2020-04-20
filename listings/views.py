from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta, date
from django.db.models import Q
from .models import Listing, Category
from django.contrib.auth.models import User
from accounts.mixins import AictiveUserRequiredMixin
from .forms import AddListingForm
from taggit.models import Tag
from django.views import generic
from django.views import View

# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        conext = {
            'title': 'Home'
        }
        return render(request, 'listings/home.html', conext)


class CategoryListing(generic.ListView):
    model = Listing
    context_object_name = 'listing_list'
    paginate_by = 10
    template_name = 'listings/liting_list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category_obj = get_object_or_404(Category, slug=category_slug)

        today = datetime.now().date()

        listing_list = Listing.active_objects.filter(
            Q(category=category_obj, booked=False, start_time__gte=today) |
            Q(category=category_obj, booked=False, end_time__lte=today)
        )

        return listing_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        context['title'] = f'{category_slug} Listings'
        return context


class TagListing(generic.ListView):
    model = Listing
    context_object_name = 'listing_list'
    paginate_by = 10
    template_name = 'listings/liting_list.html'

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        tag_obj = get_object_or_404(Tag, slug=tag_slug)

        today = datetime.now().date()

        listing_list = Listing.active_objects.filter(
            Q(tags=tag_obj, booked=False, start_time__gte=today) |
            Q(tags=tag_obj, booked=False, end_time__lte=today)
        )
        return listing_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('slug')
        context['title'] = f'{tag_slug} Listings'
        return context


class UserListing(generic.ListView):
    model = Listing
    context_object_name = 'listing_list'
    paginate_by = 10
    template_name = 'listings/user_list.html'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user_obj = get_object_or_404(User, username=username)

        today = datetime.now().date()

        listing_list = Listing.active_objects.filter(
            Q(owner=user_obj, booked=False, start_time__gte=today) |
            Q(owner=user_obj, booked=False, end_time__lte=today)
        )
        return listing_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user_obj = get_object_or_404(User, username=username)
        context['title'] = f"{username.title()}'s Listings"
        context['user_obj'] = user_obj
        return context


class ListingDetails(generic.DetailView):
    model = Listing
    template_name = 'listings/listing_details.html'

    # def get_queryset(self):
    #     listing_slug = self.kwargs.get('slug')
    #     listing = Listing.objects.filter(slug=listing_slug)
    #     return listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['related_listings'] = list(
            Listing.active_objects.filter(category=self.object.category, active=True))[:3]
        return context


class AddListing(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        add_listing_form = AddListingForm()
        context = {
            'title': 'Add Listing',
            'add_listing_form': add_listing_form
        }

        return render(request, 'listings/add_listing.html', context)

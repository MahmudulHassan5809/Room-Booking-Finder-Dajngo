from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .models import Listing, Category, ListingImage
from django.contrib.auth.models import User
from accounts.mixins import AictiveUserRequiredMixin
from .forms import AddListingForm, EditListingForm
from django.urls import reverse_lazy
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
            category=category_obj, booked=False).filter(Q(end_time__gte=today) | Q(end_time=None))

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
            tags=tag_obj, booked=False, end_time__gte=today)
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

        listing_list = Listing.active_objects.filter(owner=user_obj)
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

    def post(self, request, *args, **kwargs):
        add_listing_form = AddListingForm(request.POST, request.FILES)

        context = {
            'title': 'Add Listing',
            'add_listing_form': add_listing_form
        }
        if add_listing_form.is_valid():
            facility_name = request.POST.getlist('facility_name')
            facility_status_choice = request.POST.getlist(
                'facility_status_choice')

            add_listing = add_listing_form.save(commit=False)
            add_listing.owner = request.user
            add_listing.save()

            add_listing_form.save_m2m()

            for afile in request.FILES.getlist('images'):
                add_listing.listing_images.create(image=afile)

            for i in range(len(facility_name)):
                add_listing.listing_extras.create(
                    facility_name=facility_name[i], status=facility_status_choice[i])

            messages.success(request, 'Listing Added Successfully....')
            return redirect('listings:add_listing')
        else:
            return render(request, 'listings/add_listing.html', context)


class EditListing(AictiveUserRequiredMixin, generic.edit.UpdateView):
    model = Listing
    # fields = ['title', 'price', 'description', 'rooms', 'wash_rooms',
    #           'area', 'status', 'category', 'start_time', 'end_time', 'city', 'zip_code', 'tags']
    form_class = EditListingForm
    template_name = 'accounts/update_listing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['images'] = self.object.listing_images
        context['extras'] = self.object.listing_extras
        context['slug'] = self.kwargs.get('slug')
        return context


class UpdateListingImage(AictiveUserRequiredMixin, View):
    def post(self, request, *area, **kwargs):
        listing_slug = self.kwargs.get('slug')
        listing_obj = get_object_or_404(Listing, slug=listing_slug)

        image_count = listing_obj.listing_images.all().count()
        new_image_count = len(request.FILES.getlist('images'))

        if new_image_count == 0:
            messages.error(request, 'Please Select Some Image')
            return redirect('listings:edit_listing', listing_slug)
        elif image_count >= 4:
            messages.error(request, 'Please Delete Images To New One')
            return redirect('listings:edit_listing', listing_slug)
        elif image_count == 3 and new_image_count > 1:
            messages.error(request, 'You Can Add One More Image')
            return redirect('listings:edit_listing', listing_slug)
        elif image_count == 2 and new_image_count > 2:
            messages.error(request, 'You Can Add Two More Image')
            return redirect('listings:edit_listing', listing_slug)
        elif image_count == 1 and new_image_count > 3:
            messages.error(request, 'You Can Add Three More Image')
            return redirect('listings:edit_listing', listing_slug)
        elif image_count == 0 and new_image_count > 4:
            messages.error(request, 'You Can Add Four More Image')
            return redirect('listings:edit_listing', listing_slug)
        else:
            for afile in request.FILES.getlist('images'):
                listing_obj.listing_images.create(image=afile)
        messages.success(request, 'Image Added Successfully')
        return redirect('listings:edit_listing', listing_slug)


class DeleteListingImage(AictiveUserRequiredMixin, generic.edit.DeleteView):
    model = ListingImage
    template_name = 'listings/listingimage_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Image'
        return context

    def get_success_url(self):
        if self.kwargs != None:
            return reverse_lazy('listings:edit_listing', kwargs={'slug': self.kwargs['slug']})
        else:
            return reverse_lazy('listings:edit_listing', args=(self.object.listing.slug))

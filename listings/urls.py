from django.urls import path
from . import views

app_name = "listings"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),

    path('category/listings/<slug:slug>',
         views.CategoryListing.as_view(), name="category_listing"),

    path('tag/listings/<slug:slug>',
         views.TagListing.as_view(), name="tag_listing"),

    path('user/listings/<str:username>',
         views.UserListing.as_view(), name="user_listing"),

    path('listing/details/<slug:slug>',
         views.ListingDetails.as_view(), name="listing_details"),

]

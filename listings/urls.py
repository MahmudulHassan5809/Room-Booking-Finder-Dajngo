from django.urls import path
from . import views

app_name = "listings"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('category/rooms/<slug:slug>',
         views.CategoryRooms.as_view(), name="category_rooms"),

]

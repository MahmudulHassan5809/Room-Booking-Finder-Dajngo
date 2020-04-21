from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        success_url='accounts:dashboard',
        extra_context={
            'title': 'Login',
        }), name="login"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('my-profile/', views.MyProfile.as_view(), name="my_profile"),

    path('chanage-password/', views.ChangePassword.as_view(),
         name="change_password"),
    path('my-listing/', views.MyListing.as_view(), name="my_listing"),


    path('logout/', views.LogoutView.as_view(), name='logout'),




]
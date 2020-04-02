"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include
from django.conf import settings
from food_cloud import views
from django.conf.urls.static import static
app_name = "food_cloud"

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('index_restaurant/', views.index_restaurant, name='index_restaurant'),
    path('register_choice/', views.register_choice, name='register_choice'),
    path('register/', views.register, name='register'),
    path('register_restaurant/', views.register_restaurant,
         name='register_restaurant'),
    path('login_choice/', views.login_choice, name='login_choice'),
    path('login/', views.user_login, name='login'),
    path('login_restaurant/', views.restaurant_login, name='login_restaurant'),
    path('add_order/<meal_slug>/<meal_restaurant>/',
         views.add_order, name='add_order'),
    path('add_favourite/<meal_name_slug>',
         views.add_favourite, name='add_favourite'),
    path('remove_favourite/<meal_name_slug>',
         views.remove_favourite, name='remove_favourite'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('about_restaurant/', views.about_restaurant, name='about_restaurant'),
    path('contact/', views.contact, name='contact'),
    path('contact_restaurant/', views.contact_restaurant,
         name='contact_restaurant'),
    path('my_account/', views.my_account, name='my_account'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profile_restaurant/<username>/',
         views.ProfileView_restaurant.as_view(), name='profile_restaurant'),
    path('add_meal/', views.add_meal, name='add_meal'),
    path('meal/<slug:meal_name_slug>/', views.show_meal, name='show_meal'),
    path('restaurant/<slug:restaurant_name_slug>/',
         views.show_restaurant, name='show_restaurant'),
    path('search/', views.search, name='search'),
    path('search_restaurant/', views.search_restaurant, name='search_restaurant'),
    path('search_restaurants/',
         views.search_restaurants, name='search_restaurants'),
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('restricted/', views.restricted, name='restricted'),
    path('rate_meal/<meal_slug>/<meal_restaurant>/', views.rate_meal, name='rate_meal'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

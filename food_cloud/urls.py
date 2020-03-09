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
	path('about/', views.about, name='about'),
	path('add_meal/', views.add_meal, name='add_meal'),
	path('meal/<slug:meal_name_slug>/', views.show_meal, name='show_meal'),
	path('search/', views.search, name='search'),
	path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
	path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
	path('restricted/', views.restricted, name='restricted'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

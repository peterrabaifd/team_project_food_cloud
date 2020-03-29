from django.contrib import admin
from food_cloud.models import *

class RestaurantAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('restaurant_name',)}

class MealAdmin(admin.ModelAdmin):
	list_display = ('meal_name', 'restaurant_slug')

admin.site.register(Category)
admin.site.register(Meal, MealAdmin)
admin.site.register(UserProfile)
admin.site.register(RestaurantProfile, RestaurantAdmin)
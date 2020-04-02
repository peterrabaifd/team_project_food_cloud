from django.contrib import admin
from food_cloud.models import *

class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('restaurant_name',)
	prepopulated_fields = {'slug':('restaurant_name',)}

class MealAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('meal_name',)}
	list_display = ('meal_name', 'restaurant_slug', 'num_orders')

class RatingAdmin(admin.ModelAdmin):
	list_display = ('meal', 'rating')

admin.site.register(Category)
admin.site.register(Meal, MealAdmin)
admin.site.register(UserProfile)
admin.site.register(RestaurantProfile, RestaurantAdmin)
admin.site.register(Rating, RatingAdmin)
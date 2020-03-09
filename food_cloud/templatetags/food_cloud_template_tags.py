from django import template
from food_cloud.models import Category

register = template.Library()

@register.inclusion_tag('food_cloud/categories.html')
def get_category_list(current_category=None):
	return {'categories': Category.objects.all(), 'current_category': current_category}
	
@register.inclusion_tag('food_cloud/meals.html')
def get_meal_list(current_meal=None):
	return {'meals': Meal.objects.all(), 'current_meal': current_meal}
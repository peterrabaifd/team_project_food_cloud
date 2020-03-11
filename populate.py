import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_project_food_cloud.settings')

import django
import random
django.setup()
from food_cloud.models import *

def populate():

	meals = {'Test_meal_1': {'description': "Test_meal_1 description", 'price': 15, 'restaurant_id': 0, 'picture': "static/images/meal_default.jpg"}, 
			'Test_meal_2': {'description': "Test_meal_2 description", 'price': 15, 'restaurant_id': 0, 'picture': "static/images/meal_default.jpg"},
			'Test_meal_3': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_id': 0, 'picture': "static/images/meal_default.jpg"} }


	for cat, cat_data in meals.items():
		c = add_meal(cat, cat_data['description'], cat_data['price'], cat_data['restaurant_id'], cat_data['picture'])


def add_meal(meal_name, description, price, restaurant_id, picture):
	c = Meal.objects.get_or_create(meal_id=random.randrange(1000,10000,1), meal_name=meal_name, description=description, price=price, restaurant_id=restaurant_id, picture=picture)[0]
	c.save()
	return c
			
# def add_page(cat, title, url, views=0):
	# p = Page.objects.get_or_create(category=cat, title=title)[0]
	# p.url=url
	# p.views=views
	# p.save()
	# return p
	
# def add_cat(name, views=0, likes=0):
	# c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
	# c.save()
	# return c
	
# Start execution here!
if __name__ == '__main__':
	print('Starting population script...')
	populate()
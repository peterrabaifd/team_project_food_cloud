from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from food_cloud.models import *
from django.template.defaultfilters import slugify
from django.urls import reverse

class MealMethodTests(TestCase):
	def setUp(self):
		# self.r = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="Clucky's"), restaurant_name="Clucky's", type="Chicken", slug='')
		self.r, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="Clucky's"), restaurant_name="Clucky's", type="Chicken", slug=slugify("Clucky's"))
		print(self.r)
		
	def test_ensure_meal_prices_are_positive(self):
		meal = Meal(meal_name='Test_meal', description="Test_meal_1 description", price=15, restaurant_slug="cluckys", picture="static/images/meal_default.jpg", average_rating=4, num_orders=5)
		meal.save()
		self.assertEqual((meal.price >= 0), True)
	
	def test_slug_line_creation(self):
		self.assertEqual(self.r.slug, 'cluckys')
		
class IndexViewTests(TestCase):
	def test_index_view_with_no_categories(self):
		"""
		If no categories exist, the appropriate message should be displayed.
		"""
		response = self.client.get(reverse('food_cloud:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'There are no')
		self.assertQuerysetEqual(response.context['restaurants'], [])
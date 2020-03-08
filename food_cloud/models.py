from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email_address = models.EmailField()
	picture = models.ImageField(upload_to='profile_images', blank=True)
	isCompany = models.BooleanField(default=False)
	restaurant_id = models.IntegerField(default=0)
	def __str__(self):
		return self.user.username
		
class Meal(models.Model):
	meal_id = models.UUIDField(max_length=10, primary_key=True, default=uuid.uuid4, blank=True)
	meal_name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=200, unique=False)
	price = models.IntegerField(default=0)
	restaurant_id = models.IntegerField(default=0)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.meal_name)
		while not self.meal_id:
			newid = ''.join([
				random.sample(string.letters, 2),
				random.sample(string.digits, 2),
				random.sample(string.letters, 2),
			])

			if not self.objects.filter(pk=newid).exists():
				self.meal_id = newid
		super(Meal, self).save(*args, **kwargs)
		
	class Meta:
		verbose_name_plural = 'Meals'
	
	def __str__(self):
		return self.meal_name

class Restaurant(models.Model):
	restaurant_id = models.IntegerField()
	restaurant_name = models.CharField(max_length=30, unique=True)
	type = models.CharField(max_length=30, unique=False)
	average_rating = models.IntegerField()
	
class Order(models.Model):
	user_id = models.IntegerField()
	meal_id = models.IntegerField()
	date = models.DateTimeField()
	
class Favourite(models.Model):
	user_id = models.IntegerField()
	meal_id = models.IntegerField()
	
class Rating(models.Model):
	user_id = models.IntegerField()
	restaurant_id = models.IntegerField()
	rating = models.IntegerField()
	

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'Categories'
	
	def __str__(self):
		return self.name

class Page(models.Model):
	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 200

	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=TITLE_MAX_LENGTH)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.title
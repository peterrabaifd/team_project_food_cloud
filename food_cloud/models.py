from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from statistics import mean


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.EmailField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    isCompany = models.BooleanField(default=False)
    restaurant_id = models.IntegerField(default=0)
    isRestaurant = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class RestaurantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=30, unique=False)
    isRestaurant = models.BooleanField(default=True)
    average_rating = models.FloatField(default=0)
    slug = models.SlugField(unique=True)

    def calculate_average_rating(self):
        meals = Meal.objects.filter(restaurant_slug=self.slug)
        if meals:
            meal_ratings = list()
            for meal in meals:
                if meal.average_rating > 0:
                    meal_ratings.append(meal.average_rating)
                    self.average_rating = round(mean(meal_ratings), 1)
            print("Meals Exist")
        else:
            print("No Meals Present")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.restaurant_name)
        self.calculate_average_rating()
        super(RestaurantProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.restaurant_name


class Meal(models.Model):
    meal_id = models.UUIDField(
        max_length=10, primary_key=True, default=uuid.uuid4, blank=True)
    meal_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(
        max_length=200, unique=False, blank=True)
    price = models.FloatField(default=0)
    num_orders = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0)
    restaurant_slug = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    slug = models.SlugField(unique=False)
    customers = models.ManyToManyField(
        'UserProfile', through='Order', related_name='ordered_meals', blank=True)
    customer_favourites = models.ManyToManyField(
        'UserProfile', through='Favourite', related_name='favourite_meals', blank=True)

    def calculate_orders(self):
        orders = Order.objects.filter(meal=self)
        if orders:
            order_amounts = list()
            for order in orders:
                order_amounts.append(order.amount)
            self.num_orders = sum(order_amounts)
            print("Orders Exist")

    def calculate_average_rating(self):
        ratings = Rating.objects.filter(meal=self)
        if ratings:
            meal_ratings = list()
            for rating in ratings:
                if rating.rating > 0:
                    meal_ratings.append(rating.rating)
                    self.average_rating = round(mean(meal_ratings), 1)
            print("Ratings Exist")
        else:
            print("No Ratings")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.meal_name)
        self.calculate_orders()
        self.calculate_average_rating()
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
    meal = models.ForeignKey(
        'Meal', related_name='orders', on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey('UserProfile', related_name='orders',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField()
    amount = models.PositiveIntegerField(default=1)


class Favourite(models.Model):
    meal = models.ForeignKey(
        'Meal', related_name='favourites', on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey('UserProfile', related_name='favourites',
                                 on_delete=models.CASCADE, null=True, blank=True)


class Rating(models.Model):
    meal = models.ForeignKey(
        'Meal', related_name='ratings', on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey('UserProfile', related_name='ratings',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(default=0)


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

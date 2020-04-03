from django import forms
from food_cloud.models import *
from django.contrib.auth.models import User
from food_cloud.models import *
from django.contrib.auth.forms import UserCreationForm


class MealForm(forms.ModelForm):
    meal_name = forms.CharField(
        max_length=30, help_text="Please enter the meal name.")
    description = forms.CharField(
        max_length=200, help_text="Please enter the meal description.", required=False)
    price = forms.FloatField(
        help_text="Please enter the meal price.", min_value=0.01)
    picture = forms.ImageField(
        required=False, help_text="Please upload a picture.")
    restaurant_slug = forms.SlugField(required=False, help_text="Please enter the slug of your restaurant.")

    def __init__(self, *args, **kwargs):
        self.restaurant_slug = kwargs.pop('restaurant_slug', None)
        super(MealForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(MealForm, self).save(commit=commit)
        obj.restaurant_slug = self.restaurant_slug
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Meal
        exclude = ('average_rating', 'meal_id', 'customers',
                   'customer_favourites', 'num_orders', 'slug')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class RestaurantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantProfile
        fields = ('type',)

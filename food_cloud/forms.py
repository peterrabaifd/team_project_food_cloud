from django import forms
from food_cloud.models import *
from django.contrib.auth.models import User
from food_cloud.models import *
from django.contrib.auth.forms import UserCreationForm

class MealForm(forms.ModelForm):
	meal_name = forms.CharField(max_length=30, help_text="Please enter the meal name.")
	description = forms.CharField(max_length=200, help_text="Please enter the meal description.", required=False)
	price = forms.FloatField(help_text="Please enter the meal price.", min_value=0.01)
	picture = forms.ImageField(required=False, help_text="Please upload a picture.")
	restaurant_slug = forms.SlugField(widget=forms.HiddenInput(), required=False, help_text="Please enter the name of your restaurant.")

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
		exclude = ('average_rating','meal_id', 'customers', 'customer_favourites', 'num_orders', 'slug')

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128,
	help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data
		
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
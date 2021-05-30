from django import forms
import django
from django.db.models import fields
from django.forms.models import ModelForm
from .models import article,author,category,comment
from django.contrib.auth.forms import UserCreationForm ## For Registration
from django.contrib.auth.models import User

from blogapp import models
class createForm(forms.ModelForm):
    class Meta:
        model = article
        fields=[
            'title',
            'body',
            'image',
            'category'

        ]
class userCrationFrom(UserCreationForm):
    class Meta:
        model = User
        fields=[
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',

        ]
class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'photo',
            'details'

        ]
class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = [
            'name',
            'email',
            'post_comment'

        ]
class addCategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = [
            'name',
        ]
class updateCategory(forms.ModelForm):
    class Meta:
        model = category
        fields = [
            'name'

        ]
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'image']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control mb-3',
                                              'placeholder': 'Название'}),
            'category': widgets.Select(attrs={'class': 'form-control mb-3'}),
            'description': widgets.Textarea(attrs={'class': 'form-control mb-3'}),
            'image': widgets.ClearableFileInput(attrs={'class': 'form-control mb-3'})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['description', 'grade', 'moderated']
        widgets = {
            'description': widgets.Textarea(attrs={'class': 'form-control mb-3'}),
            'grade': widgets.TextInput(attrs={'class': 'form-control mb-3',
                                              'placeholder': 'Название'}),
        }
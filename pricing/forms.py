from django import forms
from .models import Product, Component

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'group', 'price']

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'group', 'project_name']
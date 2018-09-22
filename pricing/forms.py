from django import forms
from .models import (
    Product, 
    Component,
    Project
)
import pdb

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'group', 'price']


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'project']
        #widgets = {
       #     'project':  forms.Select()
        #}


class ComponentRelationshipForm(forms.Form):
    id = forms.IntegerField(min_value=0)
    name = forms.CharField(max_length=30)
    amount = forms.IntegerField(min_value=0)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'leader', 'description']
    

class ProjectComponentForm(forms.Form):
    id = forms.IntegerField(min_value=0)
    name = forms.CharField(max_length=30)
    amount = forms.IntegerField(min_value=0)
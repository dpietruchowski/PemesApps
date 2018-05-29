from django import forms
from .models import Product, Component, ElementRelationship

def get_all_fields(instance):
    fields = list(instance().base_fields)
    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'group', 'price']

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'group', 'project_name']

class ComponentRelationshipForm(forms.ModelForm):
    element_id = forms.IntegerField(min_value=0)
    class Meta:
        model = ElementRelationship
        fields = ['amount']
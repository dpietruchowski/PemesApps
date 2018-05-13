from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(max_length=30)
    price = forms.DecimalField(
        decimal_places=2,
        max_digits=15
    )

class DependencyForm(forms.Form):
    product_id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    amount = forms.IntegerField()
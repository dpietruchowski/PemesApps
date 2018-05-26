from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(
        decimal_places=2,
        max_digits=15,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
    )

class DependencyForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    amount = forms.IntegerField()
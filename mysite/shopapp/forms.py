from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"


class CreateOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = "user", "products"
    # name = forms.CharField(max_length=100)
    # quantity = forms.IntegerField(label='Quantity', min_value=1, max_value=999)
    # price = forms.IntegerField(label='Price', min_value=1, max_value=99999999)

from django import forms
from .models import Product, Category


class ProductForm(forms.Form):
    
    """Form for the product model"""
    product_image = forms.ImageField(required=False)
    product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'productname'}))
    product_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'productdescription'}))
    product_quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'min':0}))
    product_price = forms.DecimalField(widget=forms.NumberInput(attrs={'min':0.01, 'step': 0.01}))
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'myfieldclass'})
    )
    is_active = forms.BooleanField(required=False)

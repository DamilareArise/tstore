from django import forms
from .models import Product


# class ProductForm(forms.Form):
#     title = forms.CharField(max_length=100, required=True, label='Title', widget=forms.TextInput(attrs={'placeholder': 'Title', 'class':'form-control mb-2'}))


class ProductForm(forms.ModelForm):   
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'quantity',
            'category',
            'image'
        ]
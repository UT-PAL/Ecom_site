from django import forms
from shop_app.models import Product,Reviews


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('review',)


class search(forms.Form):
    product_search = forms.CharField(max_length=255)
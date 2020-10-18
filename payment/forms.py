from django import forms
from payment.models import billing_address

class Billing_form(forms.ModelForm):
    class Meta:
        model = billing_address
        fields = ['address','zipcode','city','country']
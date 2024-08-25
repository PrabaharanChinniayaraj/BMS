from django import forms
from django.forms import formset_factory
from .models import Transaction_Sale,CustomUser,Customer,Supplier,Transaction_Buy,Product
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']
                            



class BillingForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'readonly': 'readonly'}))
    transcode = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput()) 
    transaction_id = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput()) 

    class Meta:
        model = Transaction_Sale
        fields = ['transcode', 'transaction_id', 'product', 'quantity', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # If editing an existing instance
            self.fields['price'].initial = self.instance.product.price * self.instance.quantity
            self.fields['price'].widget.attrs['value'] = self.instance.product.price * self.instance.quantity

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        if product and quantity:
            cleaned_data['price'] = product.price * quantity
        return cleaned_data


     


BillingFormSet = formset_factory(BillingForm, extra=1)  

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number']


class VendorForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['companyname','name', 'email', 'phone_number']


class PurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    transcode = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput()) 
    class Meta:
        model = Transaction_Buy
        fields = ['transcode', 'product', 'quantity',]
        widgets = {
            'transcode': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.TextInput( attrs={'class': 'form-control'}),
            'quantity':forms.NumberInput(attrs={'class': 'form-control'}),  
        }

PurchaseFormSet = formset_factory(PurchaseForm, extra=1)  




class WhatsAppMessageForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the customer"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
        help_text="Enter the message you want to send"
    )

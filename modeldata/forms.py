from django import forms
from .models import Asset,Category,Sale,Customer,Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AssetForm(forms.ModelForm):
     class Meta:
        model = Asset
        fields = ('id','title', 'date','qty','price','category','size',"description")
        widgets={
            'amount':forms.TextInput(attrs={'readonly':'readonly'})
        }

        def clean_amount(self):
            return self.instance.amount if self.instance else 0.0


class SaleForm(forms.ModelForm):
     price=forms.DecimalField(max_digits=10,decimal_places=2)
     class Meta:
        model = Sale
        fields = ('id','title','sale_date','asset','sale_qty','price','asset')

class AssetSelectForm(forms.Form):
    
    st=forms.ModelChoiceField(
        queryset=Asset.objects.all(),
        empty_label="select item",required=False)

class CustomerForm(forms.ModelForm):
    
     class Meta:
        model = Customer
        fields = ('id','first_name','last_name','phone','address','user','gender')


    

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	




    
        



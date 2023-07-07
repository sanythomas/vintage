from django import forms
from store.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import UserAddressBook

class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address','mobile','status')

# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')
from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

PASSWORDS_DONT_MATCH = 'The passwords do not match'

class RegistrationForm(forms.models.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={
			'id': 'id_registration_username',
			'placeholder': 'Enter your user ID',
			'class': 'form-control input-lg'
		}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
			'id': 'id_registration_password',
			'placeholder': 'Enter your password',
			'class': 'form-control input-lg'
		}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
			'id': 'id_registration_password2',
			'placeholder': 'Confirm your password',
			'class': 'form-control input-lg'
		}))

	class Meta:
		model = User
		fields = ('username', 'password',)

	def clean_password2(self, *args, **kwargs):
		if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
			raise ValidationError(PASSWORDS_DONT_MATCH)


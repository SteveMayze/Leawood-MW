from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationForm(forms.models.ModelForm):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password',)

	def clean_password2(self, *args, **kwargs):
		if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
			raise ValidationError("The passwords must match")


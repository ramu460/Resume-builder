from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from django.core.cache import cache
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    # reCAPTCHA v3 field
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            action='registration',  # For analytics in reCAPTCHA admin
            attrs={
                'required_score': 0.5,  # Should match settings.py
            }
        ),
        error_messages={
            'required': 'Please complete the reCAPTCHA verification'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']

        def clean_password(self):
            password1 = self.cleaned_data.get('password1')
            try:
                validate_password(password1, self.instance)
            except ValidationError as error:
                self.add_error('password', error)
            return password1        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Fixed missing parentheses
    
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomAuthenticationForm(AuthenticationForm):
    pass

class PasswordResetFormWithRecaptcha(PasswordResetForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            action='password_reset',
            attrs={'required_score': 0.5}
        ),
        error_messages={'required': 'Please complete the reCAPTCHA verification'}
    )

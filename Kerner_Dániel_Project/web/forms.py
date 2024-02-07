from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail cím", max_length=100)
    password = forms.CharField(label="Jelszó", max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ('',)

class CustomEmailValidator(EmailValidator):
    message = "Ezzel az E-mail címmel már regisztráltak"      

class RegisterForm(forms.ModelForm):
    name = forms.CharField(label="Teljes név", max_length=255)
    email = forms.EmailField(label="E-Mail cím", max_length=255, validators=[CustomEmailValidator])
    password = forms.CharField(label="Jelszó", max_length=255, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Jelszó megerősítés", max_length=255, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password', ValidationError("A két jelszó nem eggyezik!"))
            self.add_error('password_confirm', ValidationError("A két jelszó nem eggyezik!"))

        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ezzel az E-mail címmel már regisztráltak!")
        return email
    class Meta:
        model = User
        exclude = ('password_confirm',)
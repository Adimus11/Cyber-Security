from django import forms
from .models import BankUser, Transfer

class BankUserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = BankUser
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(BankUserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class BankUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class TransferForm(forms.Form):
    receiver = forms.CharField()
    amount = forms.FloatField()

from django import forms
from .models import BankUser

class BankUserRegisterForm(forms.ModelForm):
    username = forms.CharField()
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
                "Haslo się nie zgadza"
            )


class BankUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class TransferForm(forms.Form):
    receiver = forms.CharField()
    amount = forms.FloatField()

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        receiver = cleaned_data.get("receiver")

        if not BankUser.objects.filter(username=receiver).exists():
            raise forms.ValidationError(
                "Taki uzytkownik nie istniej"
            )

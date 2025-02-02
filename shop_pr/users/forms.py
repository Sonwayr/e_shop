from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Address


class CustomUserCreationForm(UserCreationForm):
    street = forms.CharField(max_length=100, required=False, label="Street")
    house_number = forms.CharField(max_length=10, required=False, label="House number")
    city = forms.CharField(max_length=50, required=False, label="City")
    country = forms.CharField(max_length=50, required=False, label="Country")
    zip_code = forms.CharField(max_length=10, required=False, label="Zip code")

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'phone_number',
        )

    def save(self, commit=True):
        # Сохраняем пользователя
        user = super().save(commit=False)

        if commit:
            user.save()

        address, created = Address.objects.get_or_create(user=user)

        address.street = self.cleaned_data['street']
        address.house_number = self.cleaned_data['house_number']
        address.city = self.cleaned_data['city']
        address.country = self.cleaned_data['country']
        address.zip_code = self.cleaned_data['zip_code']

        if commit:
            address.save()

        return user


class CustomUserChangeForm(forms.ModelForm):
    # Дополнительные поля для редактирования адреса
    street = forms.CharField(max_length=100, required=False)
    house_number = forms.CharField(max_length=10, required=False)
    city = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=50, required=False)
    zip_code = forms.CharField(max_length=10, required=False)

    class Meta:
        model = CustomUser
        fields = ('phone_number',)

    def save(self, commit=True):
        # Сохраняем пользователя
        user = super().save(commit=False)

        address, created = Address.objects.get_or_create(user=user)

        address.street = self.cleaned_data['street']
        address.house_number = self.cleaned_data['house_number']
        address.city = self.cleaned_data['city']
        address.country = self.cleaned_data['country']
        address.zip_code = self.cleaned_data['zip_code']

        # Сохраняем адрес
        if commit:
            address.save()
            user.save()

        return user




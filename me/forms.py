from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from main.models import Profile


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True, label="Электронная почта")
    first_name = forms.CharField(max_length=100, required=False, label="Имя")
    last_name = forms.CharField(max_length=100, required=False, label="Фамилия")
    username = forms.CharField(max_length=100, required=True, label="Имя пользователя")

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class EditProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'personal-image-input'}),
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label="Старый пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label="Повторите новый пароль")

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
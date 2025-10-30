from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.Form):
    full_name = forms.CharField(label='ФИО', max_length=100)
    username = forms.CharField(label='Логин', max_length=150)
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повтор пароля')
    consent = forms.BooleanField(label='Согласие на обработку персональных данных')

    def clean_full_name(self):
        name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', name):
            raise ValidationError('ФИО должно содержать только кириллицу, пробелы и дефисы.')
        return name

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError('Логин должен содержать только латиницу и дефис.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Этот логин уже занят.')
        return username

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise ValidationError('Пароли не совпадают.')
        return cleaned
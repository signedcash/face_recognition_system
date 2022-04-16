from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from sfr.models import Face, Device


class SignInUserForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input',
                                                                       'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                           'placeholder': 'Пароль'}))
    error_messages = {
        'invalid_login': "Неверные имя пользователя или пароль.",
        'inactive': "Неверные имя пользователя или пароль.",
    }


class AddFaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddFaceForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['type'].label = ''
        self.fields['img'].label = ''

    class Meta:
        model = Face
        fields = ['name', 'type', 'img']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input',
                                           'placeholder': 'Название'}),
            'type': forms.TextInput(attrs={'class': 'form-input',
                                           'placeholder': 'Описание'}),
            'img': forms.FileInput(attrs={'class': 'inputfile-c',
                                          'multiple': True}),
        }


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['img'].label = 'Загрузите тестовое изображение:'

    class Meta:
        model = Face
        fields = ['img']
        widgets = {
            'img': forms.FileInput(attrs={'class': 'inputfile-c'}),
        }


class AddDeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddDeviceForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['code'].label = ''

    class Meta:
        model = Device
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input',
                                           'placeholder': 'Название'}),
            'code': forms.TextInput(attrs={'class': 'form-input',
                                           'placeholder': 'Пароль устройства'}),
        }

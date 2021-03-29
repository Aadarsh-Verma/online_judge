from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from authy.models import Profile
from judge.models import Contest


def UniqueUser(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this name already exists')


def UniqueEmail(value):
    if User.objects.filter(email__iexact=value):
        raise ValidationError('Email already exists')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(UniqueUser)
        self.fields['email'].validators.append(UniqueEmail)

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError('Passwords do not match')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    college = forms.CharField(max_length=100)
    bio = forms.CharField(max_length=100)
    picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'college', 'bio', 'picture']

class ContestCreateForm(forms.ModelForm):
    question = forms.CharField(max_length=255)

    class Meta:
        question = forms.CharField()
        model = Contest
        fields = '__all__'

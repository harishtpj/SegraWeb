from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'input input-bordered w-full',
        })

        self.fields['email'].widget.attrs.update({
            'class': 'input input-bordered w-full',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'autocomplete': 'new-password',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'input input-bordered w-full',
            'autocomplete': 'new-password',
        })

class StyledLoginForm(AuthenticationForm):
    username = forms.CharField(
            widget=forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            })
    )

    password = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'class': 'input input-bordered w-full',
                'autocomplete': 'current-password',
            })
    )


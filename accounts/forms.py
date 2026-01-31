from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

FORM_INPUT_CLASSES = "input input-bordered w-full"
FORM_FILE_INPUT_CLASSES = "file-input file-input-bordered w-full"

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            "class": FORM_INPUT_CLASSES,
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            "class": FORM_INPUT_CLASSES,
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": FORM_INPUT_CLASSES,
        })
    )

    profile_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": FORM_FILE_INPUT_CLASSES,
            "accept": "image/*",
        })
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "profile_photo",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": FORM_INPUT_CLASSES,
        })

        self.fields["password1"].widget.attrs.update({
            "class": FORM_INPUT_CLASSES,
            "autocomplete": "new-password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": FORM_INPUT_CLASSES,
            "autocomplete": "new-password",
        })


class StyledLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": FORM_INPUT_CLASSES,
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": FORM_INPUT_CLASSES,
            "autocomplete": "current-password",
        })
    )

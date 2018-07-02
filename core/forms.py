from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm

from core.models import Message

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'file']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        message = super().save(commit=False)
        message.author = self.user
        if commit:
            message.save()
        return message


class ChatRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Benutzername', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
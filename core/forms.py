from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Benutzername', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class InventoryForm(forms.Form):
    inventory_name = forms.CharField(
        label='Inventory Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'required': 'required'
        })
    )
    group = forms.ChoiceField(label='Gruppe',
                              choices=[
                                  ('Fachgruppe Netzwerk', 'Fachgruppe Netzwerk'),
                                  ('Fachgruppe Betrieb', 'Fachgruppe Betrieb'),
                                  ('Fachgruppe Entwicklung', 'Fachgruppe Entwicklung'),
                                  ('Fachgruppe Security', 'Fachgruppe Security'),
                                  ('Fachgruppeübergreifend', 'Fachgruppeübergreifend')
                              ])
    description = forms.CharField(
        label='Description',
        max_length=100,
        widget=forms.TextInput(attrs={
            'required': 'required'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type something here...',
            'spellcheck': 'false',
            'required': 'required'
        })
    )


class JobForm(forms.Form):
    name = forms.CharField(
        label='Job Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'required': 'required'
        })
    )
    group = forms.ChoiceField(label='Gruppe',
                              choices=[
                                  ('Fachgruppe Netzwerk', 'Fachgruppe Netzwerk'),
                                  ('Fachgruppe Betrieb', 'Fachgruppe Betrieb'),
                                  ('Fachgruppe Entwicklung', 'Fachgruppe Entwicklung'),
                                  ('Fachgruppe Security', 'Fachgruppe Security'),
                                  ('Fachgruppeübergreifend', 'Fachgruppeübergreifend')
                              ])
    playbook = forms.ChoiceField(choices=[])
    inventory = forms.ChoiceField(choices=[])
    description = forms.CharField(
        label='Description',
        max_length=100,
        widget=forms.TextInput(attrs={
            'required': 'required'
        })
    )

    def __init__(self, *args, **kwargs):
        # Extrair os valores de playbook e inventory do kwargs antes de chamar super()
        playbook_choices = kwargs.pop('playbook', [])
        inventory_choices = kwargs.pop('inventory', [])
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['playbook'].choices = playbook_choices
        self.fields['inventory'].choices = inventory_choices

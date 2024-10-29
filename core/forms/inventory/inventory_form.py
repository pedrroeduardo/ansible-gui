from django import forms


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
    available_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=False
    )
    selected_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=False
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type something here...',
            'spellcheck': 'false',
            'required': 'required'
        }),
        initial='[(GROUP NAME)] \n'
                '[NAME] ansible_host=[IP-Adresse]\n'
                '[NAME] ansible_host=[IP-Adresse]\n'
                '[NAME] ansible_host=[IP-Adresse]\n\n'
                '[(GROUP NAME):vars]\n'
                'ansible_network_os=community.ciscosmb.ciscosmb\n'
                'ansible_connection=network_cli\n'
                'ansible_user="{{ ansible_username }}"\n'
                'ansible_password="{{ ansible_password }}"'
    )

    def __init__(self, *args, **kwargs):
        tag_choices = kwargs.pop('tag_choices', [])
        super(InventoryForm, self).__init__(*args, **kwargs)
        self.fields['available_tags'].choices = tag_choices
        self.fields['selected_tags'].choices = tag_choices

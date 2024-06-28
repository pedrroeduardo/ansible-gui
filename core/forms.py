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
    available_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=False
    )
    selected_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=True
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


class PlaybookDetailsForm(forms.Form):
    playbook_name = forms.CharField(
        label='Playbook Name',
        max_length=100,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    group = forms.ChoiceField(
        label='Gruppe',
        choices=[
            ('Fachgruppe Netzwerk', 'Fachgruppe Netzwerk'),
            ('Fachgruppe Betrieb', 'Fachgruppe Betrieb'),
            ('Fachgruppe Entwicklung', 'Fachgruppe Entwicklung'),
            ('Fachgruppe Security', 'Fachgruppe Security'),
            ('Fachgruppeübergreifend', 'Fachgruppeübergreifend')
        ]
    )
    description = forms.CharField(
        label='Description',
        max_length=100,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    available_tags = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    selected_tags = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
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
        selected_tag_ids = kwargs.pop('selected_tag_ids', [])
        super(PlaybookDetailsForm, self).__init__(*args, **kwargs)
        self.fields['available_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id not in selected_tag_ids]
        self.fields['selected_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id in selected_tag_ids]


class InventoryDetailsForm(forms.Form):
    inventory_name = forms.CharField(
        label='Inventory Name',
        max_length=100,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    group = forms.ChoiceField(
        label='Gruppe',
        choices=[
            ('Fachgruppe Netzwerk', 'Fachgruppe Netzwerk'),
            ('Fachgruppe Betrieb', 'Fachgruppe Betrieb'),
            ('Fachgruppe Entwicklung', 'Fachgruppe Entwicklung'),
            ('Fachgruppe Security', 'Fachgruppe Security'),
            ('Fachgruppeübergreifend', 'Fachgruppeübergreifend')
        ]
    )
    description = forms.CharField(
        label='Description',
        max_length=100,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    available_tags = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    selected_tags = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False
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
        selected_tag_ids = kwargs.pop('selected_tag_ids', [])
        super(InventoryDetailsForm, self).__init__(*args, **kwargs)
        self.fields['available_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id not in selected_tag_ids]
        self.fields['selected_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id in selected_tag_ids]





class PlaybookForm(forms.Form):
    inventory_name = forms.CharField(
        label='Playbook Name',
        max_length=100,
        widget=forms.TextInput(attrs={'required': 'required'})
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
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    available_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=False
    )
    selected_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=True
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type something here...',
            'spellcheck': 'false',
            'required': 'required'
        }),
        initial='---\n'
                '- name: [PLAYBOOK NAME]\n'
                '  hosts: all\n'
                '  gather_facts: no\n\n'
                '  vars_files:\n'
                '    - credentials.yml\n\n'
                '  tasks:\n'
                '    - name: [TASK NAME]\n'
                '      community.ciscosmb.command:\n'
                '        commands:\n'
                '          - sh run\n'
                '      register: sh_run_output\n\n'
                '    - name: Print command output\n'
                '      debug:\n'
                '        var: sh_run_output.stdout\n'
    )

    def __init__(self, *args, **kwargs):
        tag_choices = kwargs.pop('tag_choices', [])
        super(PlaybookForm, self).__init__(*args, **kwargs)
        self.fields['available_tags'].choices = tag_choices
        self.fields['selected_tags'].choices = tag_choices



class JobForm(forms.Form):
    name = forms.CharField(
        label='Job Name',
        max_length=100,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    group = forms.ChoiceField(label='Gruppe', choices=[
        ('Fachgruppe Netzwerk', 'Fachgruppe Netzwerk'),
        ('Fachgruppe Betrieb', 'Fachgruppe Betrieb'),
        ('Fachgruppe Entwicklung', 'Fachgruppe Entwicklung'),
        ('Fachgruppe Security', 'Fachgruppe Security'),
        ('Fachgruppeübergreifend', 'Fachgruppeübergreifend')
    ])
    playbook = forms.ChoiceField(choices=[], required=True)
    inventory = forms.ChoiceField(choices=[], required=True)
    description = forms.CharField(
        label='Description',
        max_length=100,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    available_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=False
    )
    selected_tags = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple, required=True
    )

    def __init__(self, *args, **kwargs):
        playbook_choices = kwargs.pop('playbook', [])
        inventory_choices = kwargs.pop('inventory', [])
        tag_choices = kwargs.pop('tag_choices', [])
        selected_tag_ids = kwargs.pop('selected_tag_ids', [])
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['playbook'].choices = playbook_choices
        self.fields['inventory'].choices = inventory_choices
        self.fields['available_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id not in selected_tag_ids]
        self.fields['selected_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id in selected_tag_ids]



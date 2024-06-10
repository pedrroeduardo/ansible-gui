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
        }),
        initial='[loh306] \n'
                'LOH306-SWT01 ansible_host=10.20.20.10\n'
                'LOH306-SWT02 ansible_host=10.20.20.11\n'
                'LOH306-SWT03 ansible_host=10.20.20.12\n\n'
                '[loh306:vars]\n'
                'ansible_network_os=community.ciscosmb.ciscosmb\n'
                'ansible_connection=network_cli\n'
                'ansible_user="{{ ansible_username }}"\n'
                'ansible_password="{{ ansible_password }}"'
    )

class PlaybookForm(forms.Form):
    inventory_name = forms.CharField(
        label='Playbook Name',
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
        }),
        initial='---\n- name: SNMP Erstellen\n  hosts: loh306\n  gather_facts: no\n\n  vars_files:\n    - credentials.yml\n\n  tasks:\n    - name: Creating SNMP\n      community.ciscosmb.command:\n        commands:\n          - sh run'
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
        playbook_choices = kwargs.pop('playbook', [])
        inventory_choices = kwargs.pop('inventory', [])
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['playbook'].choices = playbook_choices
        self.fields['inventory'].choices = inventory_choices

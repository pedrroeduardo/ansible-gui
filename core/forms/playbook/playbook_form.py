from django import forms


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
        choices=[], widget=forms.CheckboxSelectMultiple, required=False
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
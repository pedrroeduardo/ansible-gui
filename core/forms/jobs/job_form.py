from django import forms


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
        choices=[], widget=forms.CheckboxSelectMultiple, required=False
    )

    def __init__(self, *args, **kwargs):
        playbook_choices = kwargs.pop('playbook', [])
        inventory_choices = kwargs.pop('inventory', [])
        tag_choices = kwargs.pop('tag_choices', [])
        selected_tag_ids = kwargs.pop('selected_tag_ids', [])
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['playbook'].choices = playbook_choices
        self.fields['inventory'].choices = inventory_choices
        self.fields['available_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if
                                                 tag_id not in selected_tag_ids]
        self.fields['selected_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if
                                                tag_id in selected_tag_ids]
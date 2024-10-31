from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from core.forms.playbook.playbook_form import PlaybookForm
from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import get_object_or_404
import yaml
from django.conf import settings

with open(settings.CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

playbooks = config["playbooks"]

@login_required
def create_playbook(request, type):
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    playbook_type = type
    selected_playbook = next(
        (playbook_option for playbook_option in playbooks if playbook_option["type"] == playbook_type), None)

    if request.method == 'POST':
        if selected_playbook:
            form = PlaybookForm(
                request.POST,
                tag_choices=tag_choices,
                initial={"content": selected_playbook["content"]}
            )
        if form.is_valid():
            playbook_name = form.cleaned_data['inventory_name']
            group = form.cleaned_data['group']
            group_model = get_object_or_404(Group, name=group)
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']
            selected_tags = form.cleaned_data['selected_tags']

            new_playbook = Playbook()
            new_playbook.name = playbook_name
            new_playbook.group = group_model
            new_playbook.description = description
            new_playbook.content = content
            new_playbook.save()

            new_playbook.tags.set(selected_tags)
            new_playbook.save()

            return redirect('playbook')
        else:
            form.fields['available_tags'].choices = tag_choices
            form.fields['selected_tags'].choices = [(tag.id, tag.name) for tag in Tag.objects.filter(id__in=form.cleaned_data.get('selected_tags', []))]
            print("Form is invalid", form.errors)
    else:
        form = PlaybookForm(tag_choices=tag_choices, initial={'content': selected_playbook["content"]})
        form.fields['selected_tags'].choices = []

    return render(request, "createplaybook.html", {'form': form})

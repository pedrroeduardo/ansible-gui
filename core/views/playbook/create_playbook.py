from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from core.forms.playbook.playbook_form import PlaybookForm
from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import get_object_or_404


@login_required
def create_playbook(request):
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    if request.method == 'POST':
        form = PlaybookForm(request.POST, tag_choices=tag_choices)
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

            # Add the selected tags to the new playbook
            new_playbook.tags.set(selected_tags)
            new_playbook.save()

            return redirect('playbook')
        else:
            # If the form is invalid, we need to manually set the choices again
            form.fields['available_tags'].choices = tag_choices
            form.fields['selected_tags'].choices = [(tag.id, tag.name) for tag in Tag.objects.filter(id__in=form.cleaned_data.get('selected_tags', []))]
            print("Form is invalid", form.errors)
    else:
        form = PlaybookForm(tag_choices=tag_choices)
        form.fields['selected_tags'].choices = []  # Ensure selected tags are initially empty

    return render(request, "createplaybook.html", {'form': form})
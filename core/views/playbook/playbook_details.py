from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from core.forms.playbook.playbook_details_form import PlaybookDetailsForm
from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import get_object_or_404


@login_required
def item_playbook_details(request, id):
    playbook = get_object_or_404(Playbook, pk=id)
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]
    selected_tag_ids = list(playbook.tags.values_list('id', flat=True))

    if request.method == 'POST':
        action = request.POST.get('action')
        submitted_tag_ids = request.POST.getlist('selected_tags')
        all_selected_ids = list(set(selected_tag_ids + [int(tag_id) for tag_id in submitted_tag_ids]))
        form = PlaybookDetailsForm(request.POST, tag_choices=tag_choices, selected_tag_ids=all_selected_ids)
        if form.is_valid():
            if action == 'edit':
                playbook.name = form.cleaned_data['playbook_name']
                playbook.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                playbook.description = form.cleaned_data['description']
                playbook.content = form.cleaned_data['content']
                playbook.save()
                playbook.tags.set(Tag.objects.filter(id__in=form.cleaned_data['selected_tags']))
                return redirect('playbook')
            elif action == 'delete':
                playbook.delete()
                return redirect('playbook')
            elif action == 'cancel':
                return redirect('playbook')
        else:
            print("Form invalid", form.errors)
            print("Submitted data:", request.POST)
            print("Tag choices:", tag_choices)
            print("Selected tag ids:", selected_tag_ids)
    else:
        initial_data = {
            'playbook_name': playbook.name,
            'group': playbook.group.name if playbook.group else None,
            'description': playbook.description,
            'content': playbook.content
        }
        form = PlaybookDetailsForm(initial=initial_data, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)

    return render(request, 'detailsplaybook.html', {'form': form, 'playbook': playbook})

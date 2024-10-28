from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from core.forms.inventory.inventory_details_form import InventoryDetailsForm
from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import get_object_or_404


@login_required
def item_inventory_details(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]
    selected_tag_ids = list(inventory.tags.values_list('id', flat=True))

    if request.method == 'POST':
        action = request.POST.get('action')
        submitted_tag_ids = request.POST.getlist('selected_tags')
        all_selected_ids = list(set(selected_tag_ids + [int(tag_id) for tag_id in submitted_tag_ids]))
        form = InventoryDetailsForm(request.POST, tag_choices=tag_choices, selected_tag_ids=all_selected_ids)
        if form.is_valid():
            if action == 'edit':
                inventory.name = form.cleaned_data['inventory_name']
                inventory.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                inventory.description = form.cleaned_data['description']
                inventory.content = form.cleaned_data['content']
                selected_tags = form.cleaned_data['selected_tags']
                inventory.save()
                inventory.tags.set(Tag.objects.filter(id__in=selected_tags))
                return redirect('inventory')
            elif action == 'delete':
                inventory.delete()
                return redirect('inventory')
            elif action == 'cancel':
                return redirect('inventory')
        else:
            print("Form invalid", form.errors)
            print("Submitted data:", request.POST)
            print("Tag choices:", tag_choices)
            print("Selected tag ids:", selected_tag_ids)
    else:
        initial_data = {
            'inventory_name': inventory.name,
            'group': inventory.group.name if inventory.group else None,
            'description': inventory.description,
            'content': inventory.content
        }
        form = InventoryDetailsForm(initial=initial_data, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)

    return render(request, 'details.html', {'form': form, 'inventory': inventory})
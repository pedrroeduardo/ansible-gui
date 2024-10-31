from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from core.forms.inventory.inventory_form import InventoryForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import yaml
from django.conf import settings

from core.models.tag import Tag
from core.models.group import Group
from core.models.inventory import Inventory

with open(settings.CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

inventories = config["inventory"]


@login_required
def create_inventory(request, type):
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    inventory_type = type
    selected_inventory = next(
        (inventory_option for inventory_option in inventories if inventory_option["type"] == inventory_type), None)

    if request.method == 'POST':
        if selected_inventory:
            form = InventoryForm(
                request.POST,
                tag_choices=tag_choices,
                initial={"content": selected_inventory["content"]}
            )
        if form.is_valid():
            inventory_name = form.cleaned_data['inventory_name']
            group = form.cleaned_data['group']
            group_model = get_object_or_404(Group, name=group)
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']
            selected_tags = form.cleaned_data['selected_tags']

            new_inventory = Inventory()
            new_inventory.name = inventory_name
            new_inventory.group = group_model
            new_inventory.description = description
            new_inventory.content = content
            new_inventory.save()

            # Add the selected tags to the new inventory
            new_inventory.tags.set(selected_tags)
            new_inventory.save()

            return redirect('inventory')
        else:
            # If the form is invalid, we need to manually set the choices again
            form.fields['available_tags'].choices = tag_choices
            form.fields['selected_tags'].choices = [(tag.id, tag.name) for tag in Tag.objects.filter(id__in=form.cleaned_data.get('selected_tags', []))]
            print("Formulário inválido", form.errors)
    else:
        form = InventoryForm(tag_choices=tag_choices, initial={'content': selected_inventory["content"]})
        form.fields['selected_tags'].choices = []  # Ensure selected tags are initially empty

    return render(request, "createinventory.html", {'form': form})

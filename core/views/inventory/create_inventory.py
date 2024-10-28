from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from core.forms.inventory.inventory_form import InventoryForm
from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import get_object_or_404


@login_required
def create_inventory(request):
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    if request.method == 'POST':
        form = InventoryForm(request.POST, tag_choices=tag_choices)
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
        form = InventoryForm(tag_choices=tag_choices)
        form.fields['selected_tags'].choices = []  # Ensure selected tags are initially empty

    return render(request, "createinventory.html", {'form': form})
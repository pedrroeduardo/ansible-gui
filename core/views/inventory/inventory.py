from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core.models.tag import Tag
from core.models.group import Group
from core.models.inventory import Inventory


@login_required
def inventory(request):
    # Getting the user's group names
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)  # Convertendo para lista

    # Searching for the corresponding groups in the Core model
    core_groups = Group.objects.filter(name__in=user_group_names)

    tags = Tag.objects.all()

    selected_tag = request.GET.get('tag')

    if "Fachgruppe Leitung" in user_group_names:
        if selected_tag and selected_tag != 'all':
            inventory = Inventory.objects.filter(tags__name=selected_tag)
        else:
            inventory = Inventory.objects.all()
    else:
        if selected_tag and selected_tag != 'all':
            inventory = Inventory.objects.filter(group__in=core_groups, tags__name=selected_tag)
        else:
            inventory = Inventory.objects.filter(group__in=core_groups)

    return render(request, "inventory.html", {"inventory": inventory, "tags": tags})

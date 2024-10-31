from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.urls import reverse
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
def select_playbook_type(request):
    if request.method == "POST":
        playbook_type = request.POST.get("type")
        return redirect(reverse('create_playbook', args=[playbook_type]))

    return render(request, "select_playbook_type.html", {"playbooks": playbooks})

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from core.forms.jobs.job_form import JobForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from core.models.tag import Tag
from core.models.job import Job
from core.models.inventory import Inventory
from core.models.playbook import Playbook
from core.models.group import Group


@login_required
def create_job(request):
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names:
        playbook = Playbook.objects.all()
        inventory = Inventory.objects.all()
        available_tags = Tag.objects.all()
    else:
        playbook = Playbook.objects.filter(group__in=core_groups)
        inventory = Inventory.objects.filter(group__in=core_groups)
        available_tags = Tag.objects.filter(group__in=core_groups)

    playbook_choices = [(pb.id, pb.name) for pb in playbook]
    inventory_choices = [(iv.id, iv.name) for iv in inventory]
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    if request.method == 'POST':
        form = JobForm(request.POST, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices)
        if form.is_valid():
            new_job = Job()
            new_job.name = form.cleaned_data['name']
            new_job.group = get_object_or_404(Group, name=form.cleaned_data['group'])
            new_job.playbook = get_object_or_404(Playbook, id=form.cleaned_data['playbook'])
            new_job.inventory = get_object_or_404(Inventory, id=form.cleaned_data['inventory'])
            new_job.description = form.cleaned_data['description']
            new_job.save()
            new_job.tags.set(Tag.objects.filter(id__in=form.cleaned_data['selected_tags']))
            new_job.save()

            return redirect('jobs')
        else:
            # If the form is invalid, we need to manually set the choices again
            selected_tag_ids = [int(tag_id) for tag_id in request.POST.getlist('selected_tags')]
            form.fields['available_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id not in selected_tag_ids]
            form.fields['selected_tags'].choices = [(tag_id, tag_name) for tag_id, tag_name in tag_choices if tag_id in selected_tag_ids]
            print("Formulário inválido", form.errors)
    else:
        form = JobForm(playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices, selected_tag_ids=[])
        form.fields['selected_tags'].choices = []

    return render(request, "createjob.html", {'form': form})

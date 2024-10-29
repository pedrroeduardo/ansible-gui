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
def item_job_details(request, id):
    job = get_object_or_404(Job, pk=id)
    error_message = ""

    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names:
        playbook = Playbook.objects.all()
        inventory = Inventory.objects.all()
    else:
        playbook = Playbook.objects.filter(group__in=core_groups)
        inventory = Inventory.objects.filter(group__in=core_groups)

    playbook_choices = [(pb.id, pb.name) for pb in playbook]
    inventory_choices = [(iv.id, iv.name) for iv in inventory]

    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]
    selected_tag_ids = list(job.tags.values_list('id', flat=True))

    if request.method == 'POST':
        action = request.POST.get('action')
        submitted_tag_ids = request.POST.getlist('selected_tags')
        all_selected_ids = list(set(selected_tag_ids + [int(tag_id) for tag_id in submitted_tag_ids]))
        form = JobForm(request.POST, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices, selected_tag_ids=all_selected_ids)
        if form.is_valid():
            if action == 'edit':
                job.name = form.cleaned_data['name']
                job.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                job.playbook = get_object_or_404(Playbook, id=form.cleaned_data['playbook'])
                job.inventory = get_object_or_404(Inventory, id=form.cleaned_data['inventory'])
                job.description = form.cleaned_data['description']
                job.save()
                job.tags.set(Tag.objects.filter(id__in=form.cleaned_data['selected_tags']))
                return redirect('jobs')
            else:
                error_message = form.errors

        if action == 'delete':
            job.delete()
            return redirect('jobs')

        if action == 'cancel':
            return redirect('jobs')

        initial_data = {
            'name': job.name,
            'group': job.group.name if job.group else None,
            'playbook': job.playbook.id if job.playbook else None,
            'inventory': job.inventory.id if job.inventory else None,
            'description': job.description
        }
        form = JobForm(initial=initial_data, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)
    else:
        initial_data = {
            'name': job.name,
            'group': job.group.name if job.group else None,
            'playbook': job.playbook.id if job.playbook else None,
            'inventory': job.inventory.id if job.inventory else None,
            'description': job.description
        }
        form = JobForm(initial=initial_data, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)

    return render(request, 'jobdetails.html', {'form': form, 'job': job, 'error_message': error_message})

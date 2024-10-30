from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core.models.group import Group
from core.models.job_executed import JobExecuted
from core.models.tag import Tag


@login_required
def dashboard(request):
    # Getting the user's group names
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)

    # Searching for the corresponding groups in the Core model
    core_groups = Group.objects.filter(name__in=user_group_names)

    tags = Tag.objects.all()

    selected_tag = request.GET.get('tag')

    if "Fachgruppe Leitung" in user_group_names:
        if selected_tag and selected_tag != 'all':
            job_executed = JobExecuted.objects.filter(tags__name=selected_tag)
        else:
            job_executed = JobExecuted.objects.all()
    else:
        if selected_tag and selected_tag != 'all':
            job_executed = JobExecuted.objects.filter(group__in=core_groups, tags__name=selected_tag)
        else:
            job_executed = JobExecuted.objects.filter(job__group__in=core_groups)

    return render(request, "dashboard.html", {"jobs": job_executed, "tags": tags})

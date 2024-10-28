from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import *


@login_required
def dashboard(request):
    # Getting the user's group names
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)

    # Searching for the corresponding groups in the Core model
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names:
        jobs_runned = JobRunned.objects.all()
    else:
        jobs_runned = JobRunned.objects.filter(job__group__in=core_groups)

    return render(request, "dashboard.html", {"jobs": jobs_runned})

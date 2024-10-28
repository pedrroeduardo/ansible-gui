from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import get_object_or_404
import re


@login_required
def create_new_job_run(request, id):
    job = get_object_or_404(Job, id=id)
    job_runned = JobRunned.objects.create(
        job=job,
        username=request.user.username,
        output="",
        status=Status.objects.get(name="Laufend")
    )
    return redirect('run-job', id=job_runned.id)


@login_required
def run_job(request, id):
    job = get_object_or_404(JobRunned, id=id)
    return render(request, 'run_job_details.html', {'job_id': id, "jobs": job})


@login_required
def details_run_job(request, id):
    job = get_object_or_404(JobRunned, id=id)

    output = re.sub(r'\\n', '\n', job.output)
    processed_output = "\n".join([line for line in output.splitlines() if line.strip() != ""])

    return render(request, 'job_details.html', {'jobs': job, 'processed_output': processed_output})

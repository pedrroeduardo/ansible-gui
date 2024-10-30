from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import re

from core.models.job import Job
from core.models.job_executed import JobExecuted
from core.models.status import Status


@login_required
def create_new_job_run(request, id):
    job = get_object_or_404(Job, id=id)
    job_runned = JobExecuted.objects.create(
        job=job,
        username=request.user.username,
        output="",
        status=Status.objects.get(name="Laufend"),
    )

    job_runned.tags.set(job.tags.all())

    return redirect('run-job', id=job_runned.id)


@login_required
def run_job(request, id):
    job = get_object_or_404(JobExecuted, id=id)
    return render(request, 'run_job_details.html', {'job_id': id, "jobs": job})


@login_required
def details_run_job(request, id):
    job = get_object_or_404(JobExecuted, id=id)

    output = re.sub(r'\\n', '\n', job.output)
    processed_output = "\n".join([line for line in output.splitlines() if line.strip() != ""])

    return render(request, 'job_details.html', {'jobs': job, 'processed_output': processed_output})

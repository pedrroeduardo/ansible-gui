from django.db import models

from core.models.job import Job
from core.models.status import Status


class JobExecuted(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_runs')
    username = models.CharField(max_length=8)
    output = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='job_runs')
    start_time = models.DateTimeField(auto_now=True)
    has_run = models.BooleanField(default=False)

    def __str__(self):
        return f"Run of {self.job.name} by {self.username} - ID #{self.id}"

    class Meta:
        verbose_name_plural = "Job Executed"

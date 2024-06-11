from django.db import models
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=23)

    def __str__(self):
        return self.name


class Playbook(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Inventories"


class Status(models.Model):
    name = models.CharField(max_length=14)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Status"


class Job(models.Model):
    name = models.CharField(max_length=100)
    playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE, related_name='jobs')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(default='')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class JobRunned(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_runs')
    username = models.CharField(max_length=8)
    output = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='job_runs')
    start_time = models.DateTimeField(auto_now=True)
    has_run = models.BooleanField(default=False)

    def __str__(self):
        return f"Run of {self.job.name} by {self.username}"

    class Meta:
        verbose_name_plural = "Job Runs"


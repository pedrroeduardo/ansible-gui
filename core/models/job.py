from django.db import models

from core.models.playbook import Playbook
from core.models.inventory import Inventory
from core.models.group import Group
from core.models.tag import Tag


class Job(models.Model):
    name = models.CharField(max_length=100)
    playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE, related_name='jobs')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(default='')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='job_tags', blank=True)

    def __str__(self):
        return self.name

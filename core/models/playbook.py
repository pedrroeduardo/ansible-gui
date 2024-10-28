from django.db import models

from core.models.group import Group
from core.models.tag import Tag


class Playbook(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='playbook_tags', blank=True)

    def __str__(self):
        return self.name

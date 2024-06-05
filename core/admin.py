from django.contrib import admin
from .models import Playbook, Inventory, Group, Status, Job, JobRunned

# Register your models here.
admin.site.register(Playbook)
admin.site.register(Inventory)
admin.site.register(Group)
admin.site.register(Status)
admin.site.register(Job)
admin.site.register(JobRunned)

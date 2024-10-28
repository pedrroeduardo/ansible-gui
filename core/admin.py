from django.contrib import admin
from core.models.job import Job
from core.models.playbook import Playbook
from core.models.inventory import Inventory
from core.models.tag import Tag
from core.models.group import Group
from core.models.status import Status
from core.models.job_executed import JobExecuted



@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'playbook', 'inventory', 'group', 'last_modified')
    search_fields = ('name', 'description')
    list_filter = ('group', 'last_modified', 'tags')
    filter_horizontal = ('tags',)


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'group', 'last_modified')
    search_fields = ('name', 'description')
    list_filter = ('group', 'last_modified')
    filter_horizontal = ('tags',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'group', 'last_modified')
    search_fields = ('name', 'description')
    list_filter = ('group', 'last_modified')
    filter_horizontal = ('tags',)


admin.site.register(Group)
admin.site.register(Status)
admin.site.register(JobExecuted)
admin.site.register(Tag)

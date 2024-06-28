from django.contrib import admin
from .models import *


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
admin.site.register(JobRunned)
admin.site.register(Tag)

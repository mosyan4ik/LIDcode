from django.contrib import admin
from .models import Event, Organizers, Sponsors
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'timetable')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('status',)
    list_filter = ('status',)

class OrganizersAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

class SponsorsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Event, EventAdmin)
admin.site.register(Organizers, OrganizersAdmin)
admin.site.register(Sponsors, SponsorsAdmin)
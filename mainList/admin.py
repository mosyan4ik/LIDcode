from django.contrib import admin
from .models import *
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_display_links = ('name',)
    search_fields = ('name',)
    filter_horizontal = ['sponsors', 'organizers']
    # list_editable = ('id',)
    # list_filter = ('id',)

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
admin.site.register(Participant)
admin.site.register(Team)
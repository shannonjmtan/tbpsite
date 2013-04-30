from django.contrib import admin
from event.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'term', 'name', 'start', 'end', 'event_type', 'dropdown')
    list_editable = ('dropdown',)
    filter_horizontal = ('attendees',)

admin.site.register(Event, EventAdmin)

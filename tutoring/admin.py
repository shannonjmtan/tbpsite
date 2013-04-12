from django.contrib import admin
from tutoring.models import *

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'comment') 
    def __init__(self, *args, **kwargs):
        super(FeedbackAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

class TutoringAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'term', 'day_1', 'day_2')
    list_editable = ('day_1', 'day_2')

class WeekAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'term', 'day_1', 'day_2', 'hours', 'tutees')
    list_editable = ('hours', 'tutees')
    
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Tutoring, TutoringAdmin)
admin.site.register(Week3, WeekAdmin)
admin.site.register(Week4, WeekAdmin)
admin.site.register(Week5, WeekAdmin)
admin.site.register(Week6, WeekAdmin)
admin.site.register(Week7, WeekAdmin)
admin.site.register(Week8, WeekAdmin)
admin.site.register(Week9, WeekAdmin)

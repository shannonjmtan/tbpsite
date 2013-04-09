from django.contrib import admin
from app.models import Term, Current, Profile, Feedback

class CurrentAdmin(admin.ModelAdmin):
    list_display = ['term']
    list_editable = ['term']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'position', 'house', 'major', 'initiation_term', 'graduation_term']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'comment']

    def __init__(self, *args, **kwargs):
        super(FeedbackAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

admin.site.register(Term)
admin.site.register(Current)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Feedback, FeedbackAdmin)

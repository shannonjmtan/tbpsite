from django.contrib import admin
from app.models import Profile, Feedback

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'major', 'graduation_year']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'comment']

    def __init__(self, *args, **kwargs):
        super(FeedbackAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Feedback, FeedbackAdmin)

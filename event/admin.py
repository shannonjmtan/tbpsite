from django.contrib import admin
from social.models import Social

class SocialAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'term')
    filter_horizontal = ('attendees',)

admin.site.register(Social, SocialAdmin)

from django.contrib import admin
from app.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'major', 'graduation_year']

admin.site.register(Profile, ProfileAdmin)

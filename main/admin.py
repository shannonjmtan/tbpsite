from django import forms
from django.contrib import admin
from main.models import *
from tutoring.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ObjectDoesNotExist

def create_profile(modeladmin, request, queryset):
    term = Current.objects.get_term()
    if term is None:
        raise forms.ValidationError('Current term not set')
    create_candidates(modeladmin, request, 
            [Profile.objects.get_or_create(user=user)[0] 
                for user in queryset])

def create_candidates(modeladmin, request, queryset):
    term = Current.objects.get_term()
    if term is None:
        raise forms.ValidationError('Current term not set')

    # check for errors, all or nothing
    for profile in queryset:
        if profile.position == '1':
            raise forms.ValidationError('User is already a member')

        try:
            candidate = Candidate.objects.get(profile=profile)
            raise forms.ValidationError(
                    'User is already a candidate')
        except ObjectDoesNotExist:
            pass

    for profile in queryset:
        create_candidate(profile, term)

def create_candidate(profile, term):
    week_3 = Week3.objects.get_or_create(profile=profile, term=term)[0]
    week_4 = Week4.objects.get_or_create(profile=profile, term=term)[0]
    week_5 = Week5.objects.get_or_create(profile=profile, term=term)[0]
    week_6 = Week6.objects.get_or_create(profile=profile, term=term)[0]
    week_7 = Week7.objects.get_or_create(profile=profile, term=term)[0]
    week_8 = Week8.objects.get_or_create(profile=profile, term=term)[0]
    week_9 = Week9.objects.get_or_create(profile=profile, term=term)[0]
    tutoring = Tutoring.objects.get_or_create(profile=profile, term=term,
            week_3=week_3,
            week_4=week_4,
            week_5=week_5,
            week_6=week_6,
            week_7=week_7,
            week_8=week_8,
            week_9=week_9)[0]
    candidate = Candidate.objects.get_or_create(profile=profile, term=term, 
            tutoring=tutoring)[0]

class MyUserAdmin(UserAdmin):
    actions = (create_profile,)

class HousePointsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'term', 'resume', 'professor_interview', 'other')
    list_editable = ('resume', 'professor_interview', 'other')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'position', 'house', 'major', 'initiation_term', 'graduation_term')
    actions = (create_candidates,)

class CandidateAdmin(admin.ModelAdmin):
    list_display = (
            '__unicode__', 'term', 'bent_polish', 'candidate_quiz', 'candidate_meet_and_greet', 
            'signature_book', 'community_service', 'initiation_fee', 
            'engineering_futures')
    list_editable = (
            'bent_polish', 'candidate_quiz', 'candidate_meet_and_greet', 
            'signature_book', 'community_service', 'initiation_fee', 
            'engineering_futures') 

class ActiveMemberAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'term', 'requirement_choice', 'requirement_complete')
    list_editable = ('requirement_choice', 'requirement_complete')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Term)
admin.site.register(Current)
admin.site.register(HousePoints, HousePointsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(ActiveMember, ActiveMemberAdmin)

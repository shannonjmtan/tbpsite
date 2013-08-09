from django import forms
from django.contrib import admin
from main.models import *
from tutoring.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

def generate_profile(user):
    return Profile.objects.get_or_create(user=user)[0]

def generate_candidate(profile, term):
    tutoring = generate_tutoring(profile, term)
    return Candidate.objects.get_or_create(profile=profile, term=term, 
            tutoring=tutoring)[0]

def generate_active_member(profile, term):
    tutoring = create_Tutoring(profile, term)
    return ActiveMember.objects.get_or_create(profile=profile, term=term,
            tutoring=tutoring)[0]

def generate_tutoring(profile, term):
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
    return tutoring

class MyUserAdmin(UserAdmin):
    actions = ('create_profile', 'reset_password')

    def create_profile(self, request, queryset):
        for user in queryset:
            generate_profile(user)

    def reset_password(self, request, queryset):
        for user in queryset:
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            send_mail('TBP Account Password Reset', 
                    'Welcome to UCLA Tau Beta Pi!\n'
                    'Our website can be found at http://tbp.seas.ucla.edu\n'
                    '\n'
                    'Username: %s\n'
                    'Password: %s\n'
                    '\n'
                    'This account is used for uploading your resume and professor interview.\n'
                    'You can find your profile by clicking your username at the top right corner after logging in.\n'
                    'Please change your password and update your information so we can keep the resumes we send out up to date.\n'
                    '\n'
                    'Bryan Ngo\n'
                    'Webmaster - Tau Beta Pi\n'
                    'UCLA - CA Epsilon\n' % (user.get_username(), password),
                    'bngo92@gmail.com', [user.email], fail_silently=False)

class HousePointsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'term', 'resume', 'professor_interview', 
            'other')
    list_editable = ('resume', 'professor_interview', 'other')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'position', 'house', 'major', 
            'initiation_term', 'graduation_term', 'resume_pdf', 'resume_word',
            'professor_interview')
    list_filter = ('position',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    actions = ('create_candidate', 'create_active_member')

    def create_candidate(self, request, queryset):
        term = Current.objects.get_term()
        if term is None:
            self.message_user(request, 'Current term not set')

        # check for errors, all or nothing
        for profile in queryset:
            if profile.position == '1':
                self.message_user(request, profile.__unicode__() + 
                        ' is already a member')
                return

            try:
                candidate = Candidate.objects.get(profile=profile)
                self.message_user(request, profile.__unicode__() + 
                        ' is already a candidate')
                return
            except ObjectDoesNotExist:
                pass

        for profile in queryset:
            generate_candidate(profile, term)

    def create_active_member(modeladmin, request, queryset):
        term = Current.objects.get_term()
        if term is None:
            self.message_user(request, 'Current term not set')

        for profile in queryset:
            generate_active_member(profile, term)

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

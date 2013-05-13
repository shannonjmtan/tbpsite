from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.models import Profile, Term, Candidate
from tutoring.models import Tutoring
from tbpsite.settings import BASE_DIR
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core.exceptions import ObjectDoesNotExist
from web.views import render_next
import datetime

class Error:
    def __init__(self):
        self.incorrect_password = False
        self.username_taken = False
        self.non_matching_password = False
        self.resume_too_big = False
        self.wrong_resume_type = False
        self.interview_too_big = False
        self.wrong_interview_type = False

    def error(self):
        return (self.incorrect_password or self.username_taken or 
                self.non_matching_password or self.resume_too_big or
                self.wrong_resume_type or self.interview_too_big or
                self.wrong_interview_type)

def get_next(request):
    """ Return the next parameter from get.
    If it does not exist or it is the empty string,
    return the path to the root.
    """

    next = request.GET.get('next', '/')
    if not next:
        next = '/'
    return next

def login(request):
    next = get_next(request)
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    error = True
    if username and password:
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            error = False
    return redirect(next + ('' if not error else '?error=True'))

def logout(request):
    next = get_next(request)
    auth.logout(request)
    return redirect(next)

def profile(request):
    next = get_next(request)
    if not request.user.is_authenticated():
        return redirect(next)

    user = request.user
    profile = Profile.objects.get_or_create(user=user)[0]
    term = profile.graduation_term

    error = Error()
    if request.method == "POST":
        resume = None
        professor_interview = None

        current_password = request.POST.get('current_password')
        username = request.POST.get('username')
        if user.username != username:
            if not user.check_password(current_password):
                error.incorrect_password = True
            try:
                User.objects.get(username=username)
                error.username_taken = True
            except ObjectDoesNotExist:
                pass
            user.username = username

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password or confirm_password:
            if not user.check_password(current_password):
                error.incorrect_password = True
            if new_password != confirm_password:
                error.non_matching_password = True
            user.set_password(new_password)
            
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        profile.major = request.POST.get('major')
        graduation_quarter = request.POST.get('graduation_quarter')
        graduation_year = request.POST.get('graduation_year')
        term = Term.objects.get_or_create(
                quarter=graduation_quarter, year=graduation_year)[0]

        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            if resume.size > 2621440: # 2.5 MB
                error.resume_too_big = True
            if (resume.content_type != 'application/pdf' and 
                    resume.content_type != 'application/force-download'):
                error.wrong_resume_type = resume.content_type
        if 'professor_interview' in request.FILES:
            professor_interview = request.FILES['professor_interview']
            if professor_interview.size > 2621440: # 2.5 MB
                error.interview_too_big = True
            if (professor_interview.content_type != 'application/pdf' and
                    professor_interview.content_type != 'application/force-download'):
                error.wrong_interview_type = True

        if not error.error():
            if resume is not None:
                with open(BASE_DIR + '/resumes/' + str(user.id), 'wb+') as f:
                    for chunk in resume.chunks():
                        f.write(chunk)
                    profile.resume = datetime.datetime.today()

            if professor_interview is not None:
                with open(BASE_DIR + '/interviews/' + str(user.id), 'wb+') as f:
                    for chunk in professor_interview.chunks():
                        f.write(chunk)
                    profile.professor_interview = datetime.datetime.today()

            profile.graduation_term = term

            user.save()
            profile.save()
            error.success = True

    majors = [item + ((' selected="selected"',) 
        if item[0] == profile.major else ('',)) 
        for item in profile.MAJOR_CHOICES]
    try:
        quarters = [item + ((' selected="selected"',) 
            if item[0] == Term.objects.get(id=term.id).quarter else ('',)) 
            for item in Term.QUARTER_CHOICES]
    except AttributeError:
        quarters = [item + ('',) for item in Term.QUARTER_CHOICES]

    return render(request, 'profile.html', 
            {'user': user,
                'profile': profile,
                'term': term,
                'majors': majors,
                'quarters': quarters,
                'error': error})

def resume(request):
    next = get_next(request)
    if not request.user.is_authenticated():
        return redirect(next)

    user = request.user
    try:
        f = open(BASE_DIR + '/resumes/' + str(user.id))
        response = HttpResponse(FileWrapper(f), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=resume.pdf'
        return response
    except IOError:
        return redirect(next)

def interview(request):
    next = get_next(request)
    if not request.user.is_authenticated():
        return redirect(next)

    user = request.user
    response = None
    try:
        f = open(BASE_DIR + '/interviews/' + str(user.id))
        response = HttpResponse(FileWrapper(f), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=interview.pdf'
        return response
    except IOError:
        return redirect(next)

def candidates(request):
    next = get_next(request)
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect(next)

    return render(request, 'candidates.html', 
            {'candidate_list': Candidate.default.order_by('profile')})

def active_members(request):
    next = get_next(request)
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect(next)

    return render(request, 'active_members.html', 
            {'member_list': ActiveMember.default.order_by('profile')})

def tutoring_hours(request):
    next = get_next(request)
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect(next)

    return render(request, 'tutoring_hours.html', 
            {'tutoring_list': Tutoring.objects.order_by('profile')})

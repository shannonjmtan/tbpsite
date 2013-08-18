import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render, redirect

from main.models import Profile, Term, Candidate, ActiveMember, House, HousePoints, Settings, MAJOR_CHOICES, DAY_CHOICES, HOUR_CHOICES
from tbpsite.settings import BASE_DIR
from tutoring.models import Tutoring, Class
from web.views import render_next

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
        return any([self.incorrect_password, self.username_taken, self.non_matching_password, self.resume_too_big,
                self.wrong_resume_type, self.interview_too_big, self.wrong_interview_type])

def get_next(request):
    """ Return the next parameter from get.
    If it does not exist or it is the empty string,
    return the path to the root.
    """

    next = request.GET.get('next', '/')
    if not next:
        next = '/'
    return next

def redirect_next(request, query=''):
    return redirect('{}{}'.format(get_next(request), query))

def validate_file(f, mime_types, error):
    ret = True
    if f.size > 2621440: # 2.5 MB
        error.resume_too_big = True
        ret = False
    if f.content_type not in mime_types:
        error.wrong_resume_type = f.content_type
        ret = False
    return ret

def write_file(upload, save_path):
    with open(save_path, 'wb+') as f:
        for chunk in upload.chunks():
            f.write(chunk)
    return datetime.datetime.today()

def login(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    error = True
    if username and password:
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            error = False

    if error:
        return redirect_next(request, '?error=True')
    return redirect_next(request)

def logout(request):
    auth.logout(request)
    return redirect_next(request)

def profile_view(request):
    if not request.user.is_authenticated():
        return redirect_next(request)

    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if not all([user.email, user.first_name, user.last_name, profile.graduation_term and profile.graduation_term.year]):
        return redirect(edit, from_redirect='redirect')

    if profile.position == profile.CANDIDATE:
        details = ((name, 'Completed' if requirement else 'Not Completed') for name, requirement in Candidate.objects.filter(profile=profile)[0].requirements())
    else:
        details = ((active.term, 'Completed' if active.completed else 'In Progress') for active in ActiveMember.objects.filter(profile=profile))

    return render(request, 'profile.html', {'user': user, 'profile': profile, 'details': details})

def edit(request, from_redirect=''):
    if not request.user.is_authenticated():
        return redirect_next(request)

    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    term = profile.graduation_term

    error = Error()
    if request.method == "POST":
        resume_pdf = None
        resume_word = None
        professor_interview = None

        current_password = request.POST.get('current_password')
        username = request.POST.get('username')
        if username:
            user.username = username

            if not user.check_password(current_password):
                error.incorrect_password = True

            try:
                User.objects.get(username=username)
                error.username_taken = True
            except ObjectDoesNotExist:
                pass

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password or confirm_password:
            if not user.check_password(current_password):
                error.incorrect_password = True
            if new_password != confirm_password:
                error.non_matching_password = True

            if not error.incorrect_password and not error.non_matching_password:
                user.set_password(new_password)
            
        email = request.POST.get('email')
        if email:
            user.email = email
        first_name = request.POST.get('first_name')
        if first_name:
            user.first_name = first_name
        last_name = request.POST.get('last_name')
        if last_name:
            user.last_name = last_name

        profile.nickname = request.POST.get('nickname')
        profile.gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        if birthday:
            profile.birthday = birthday
        phone_number = request.POST.get('phone_number')
        if phone_number:
            profile.phone_number = phone_number
        profile.major = request.POST.get('major')
        graduation_quarter = request.POST.get('graduation_quarter')
        graduation_year = request.POST.get('graduation_year')
        if graduation_year:
            term, created = Term.objects.get_or_create(quarter=graduation_quarter, year=graduation_year)
        profile.day_1 = request.POST.get('day_1')
        profile.hour_1 = request.POST.get('hour_1')
        profile.day_2 = request.POST.get('day_2')
        profile.hour_2 = request.POST.get('hour_2')
        profile.day_3 = request.POST.get('day_3')
        profile.hour_3 = request.POST.get('hour_3')

        pdf = ('application/pdf', 'application/force-download')
        word = ('application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        if 'resume_pdf' in request.FILES:
            resume_pdf = request.FILES['resume_pdf']
            if validate_file(resume_pdf, pdf, error):
                profile.resume_pdf = write_file(resume_pdf, '{}/resumes_pdf/{}'.format(BASE_DIR, user.id))

        if 'resume_word' in request.FILES:
            resume_word = request.FILES['resume_word']
            if validate_file(resume_word, word, error):
                profile.resume_word = write_file(resume_word, '{}/resumes_word/{}'.format(BASE_DIR, user.id))

        if 'professor_interview' in request.FILES:
            professor_interview = request.FILES['professor_interview']
            if validate_file(professor_interview, pdf, error):
                profile.professor_interview = write_file(professor_interview, '{}/professor_interview/{}'.format(BASE_DIR, user.id))

        if not error.error():
            user.save()
            profile.graduation_term = term
            profile.save()
            return redirect(profile_view)

    majors = [(' value={}{}'.format(value, ' selected="selected"' if value == profile.major else ''), major) for value, major in MAJOR_CHOICES]
    quarters = [(' value={}{}'.format(value, ' selected="selected"' if term and value == term.quarter else ''), quarter) for value, quarter in Term.QUARTER_CHOICES]
    day_1 = [(' value={}{}'.format(value, ' selected="selected"' if value == profile.day_1 else ''), day) for value, day in DAY_CHOICES]
    hour_1 = [(' value={}{}'.format(value, ' selected="selected"' if value == profile.hour_1 else ''), hour) for value, hour in HOUR_CHOICES]
    day_2 = [(' value={}{}'.format(value, ' selected="selected"' if value == profile.day_2 else ''), day) for value, day in DAY_CHOICES]
    hour_2 = [(' value={}{}'.format(value, ' selected="selected"' if value == profile.hour_2 else ''), hour) for value, hour in HOUR_CHOICES]
    day_3 = [(' value={}{}'.format(value, ' selected="selected"' if value == profile.day_3 else ''), day) for value, day in DAY_CHOICES]
    hour_3 = [(' value={}{}'.format(value, ' selected="selected"' if value == profile.hour_3 else ''), hour) for value, hour in HOUR_CHOICES]

    classes = profile.classes.all()

    return render(request, 'edit.html', {'from_redirect': from_redirect, 'user': user, 'profile': profile, 'term': term, 'majors': majors, 'quarters': quarters, 'error': error,
        'day_1': day_1, 'hour_1': hour_1, 'day_2': day_2, 'hour_2': hour_2, 'day_3': day_3, 'hour_3': hour_3})

def add(request):
    departments = (department for department, _ in Class.DEPT_CHOICES)
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        dept = request.POST.get('dept')
        cnums = request.POST.get('cnum')
        if cnums:
            for cnum in cnums.split(','):
                profile.classes.add(Class.objects.get_or_create(department=dept, course_number=cnum.strip())[0])
        else:
            for cls in request.POST:
                if request.POST[cls] == 'on':
                    dept, cnum = cls.split()
                    try:
                        cls = Class.objects.get(department=dept, course_number=cnum)
                        profile.classes.remove(cls)
                    except Class.DoesNotExist:
                        pass
    
    return render(request, 'add.html', {'departments': departments, 'classes': profile.classes.all()})

def resume_pdf(request):
    if not request.user.is_authenticated():
        return redirect_next(request)

    user = request.user
    try:
        f = open(BASE_DIR + '/resumes_pdf/' + str(user.id))
        response = HttpResponse(FileWrapper(f), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=resume.pdf'
        return response
    except IOError:
        return redirect_next(request)

def resume_word(request):
    if not request.user.is_authenticated():
        return redirect_next(request)

    user = request.user
    try:
        f = open(BASE_DIR + '/resumes_word/' + str(user.id))
        response = HttpResponse(FileWrapper(f), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename=resume.doc'
        return response
    except IOError:
        return redirect_next(request)

def interview(request):
    if not request.user.is_authenticated():
        return redirect_next(request)

    user = request.user
    response = None
    try:
        f = open(BASE_DIR + '/interviews/' + str(user.id))
        response = HttpResponse(FileWrapper(f), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=interview.pdf'
        return response
    except IOError:
        return redirect_next(request)

def candidates(request):
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect_next(request)

    return render(request, 'candidates.html', {'candidate_list': Candidate.current.order_by('profile')})

def active_members(request):
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect_next(request)

    return render(request, 'active_members.html', {'member_list': ActiveMember.current.order_by('profile')})

def tutoring_hours(request):
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect_next(request)

    return render(request, 'tutoring_hours.html', {'tutoring_list': Tutoring.objects.order_by('profile')})

def houses(request):
    term = Settings.objects.term()
    house_points = [HousePoints.objects.get_or_create(house=house, term=term)[0] for house in House.objects.all()]
    return render(request, 'houses.html', {'houses': house_points})

def downloads(request):
    if not request.user.is_authenticated():
        return redirect_next(request)

    return render(request, 'downloads.html')

def spreadsheet(request):
    if not request.user.is_authenticated():
        return redirect_next(request)

    data = '\n'.join(['First Name,Last Name,Email,Nickname,Gender,Birthday,Phone Number,Major,Initiation Term,Graduation Term'] + 
            [profile.dump() for profile in Profile.objects.all() if profile.user.id != 1])
    response = HttpResponse(data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=spreadsheet.csv'
    return response

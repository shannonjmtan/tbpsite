from django.shortcuts import render, redirect
from django.contrib import auth
from app.models import Profile
from django.core.exceptions import ObjectDoesNotExist

def get_next(request):
    """ Return the next parameter from get.
    If it does not exist or it is the empty string,
    return the path to the root.
    """

    next = request.GET.get('next', '/')
    if not next:
        next = '/'
    return next

def render_next(request, template_name):
    return render(request, template_name, 
            {'user': request.user, 
                'next': request.path})

def home(request):
    return render_next(request, 'home.html')

def events(request): 
    return render_next(request, 'events.html')

def poker_tournament(request):
    return render_next(request, 'poker_tournament.html')

def rube_goldberg(request):
    return render_next(request, 'rube_goldberg.html')

def requirements(request):
    return render_next(request, 'requirements.html')

def tutoring(request):
    return render_next(request, 'tutoring.html')

def programs(request):
    return render_next(request, 'programs.html')

def emcc(request):
    return render_next(request, 'emcc.html')

def fe(request):
    return render_next(request, 'fe.html')

def about(request):
    return render_next(request, 'about.html')

def awards(request):
    return render_next(request, 'awards.html')

def officers(request):
    return render_next(request, 'officers.html')

def faculty(request):
    return render_next(request, 'faculty.html')

def contact(request):
    return render_next(request, 'contact.html')

def eligibility_list(request):
    return render_next(request, 'eligibility_list.html')

def houses(request):
    return render_next(request, 'houses.html')

def login(request):
    next = get_next(request)
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    if username and password:
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
    return redirect(next)

def logout(request):
    next = get_next(request)
    auth.logout(request)
    return redirect(next)

def profile(request):
    next = get_next(request)
    if not request.user.is_authenticated():
        return redirect(next)

    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = Profile(user=user)
        profile.save()
    return render(request, 'profile.html', 
            {'user': user,
                'profile': profile})

def update(request):
    next = get_next(request)
    if request.user.is_authenticated():
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.major = request.POST.get('major')
        user.save()
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            profile = Profile(user=user)
        profile.graduation_year = request.POST.get('graduation_year')
        profile.save()
    return redirect(next)

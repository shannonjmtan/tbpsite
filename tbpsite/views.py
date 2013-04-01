from django.shortcuts import render, redirect
from django.contrib import auth

def render_next(request, template_name):
    return render(request, template_name, {'next': request.path})

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
    next = request.GET.get('next', False)
    if not next:
        next = '/'
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    if username and password:
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
    return redirect(next)

def logout(request):
    next = request.GET.get('next', False)
    if not next:
        next = '/'
    auth.logout(request)
    return redirect(next)


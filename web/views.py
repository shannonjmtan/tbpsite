from django.shortcuts import render, redirect
from event.models import Event
from tutoring.models import Feedback
from main.models import Candidate

def render_next(request, template_name, additional=None):
    dictionary = {'user': request.user, 'next': request.path, 
            'events': Event.objects.filter(dropdown=True)}
    if additional is not None:
        dictionary.update(additional)
    return render(request, template_name, dictionary)

def home(request):
    return render_next(request, 'home.html')

def requirements(request):
    return render_next(request, 'requirements.html')

def tutoring(request):
    return render_next(request, 'tutoring.html')

def schedule(request):
    return render_next(request, 'tutoring_schedule.html')

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

def feedback(request):
    if request.method == "POST" and 'comment' in request.POST:
        Feedback(comment=request.POST.get('comment')).save()
    return redirect('main.views.tutoring')

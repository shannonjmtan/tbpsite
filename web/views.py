from django.shortcuts import render, redirect
from event.models import Event
from tutoring.models import Feedback
from main.models import Candidate, Faculty, Officer
import re

def render_next(request, template_name, additional=None):
    dictionary = {'user': request.user, 'next': request.path, 
            'events': Event.objects.filter(dropdown=True)}
    if additional is not None:
        dictionary.update(additional)
    return render(request, template_name, dictionary)

def home(request):
    return render_next(request, 'home.html',
            { 'upcomingEvents': sorted( Event.objects.filter(dropdown=True), 
                key=lambda event: event.start ) } )

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
    positionRe = re.compile( r'Club Liaison (\([^)]*\))' )
    positions = []
    liaisons = []
    for position in Officer.objects.all():
        match = positionRe.match( position.position )
        if match:
            for officer in position.profile.all():
                liaisons.append(' '.join([str(officer), match.group(1)]))
        else:
            positions.append( ( position.position, [ str( officer ) 
                for officer in position.profile.all() ] ) )

    positions.append( ( 'Faculty Advisor', [ 'Bill Goodin' ] ) )
    positions.append( ( 'Club Liaison', liaisons ) )

    return render_next(request, 'officers.html', {
            'term' : 'Summer - Fall 2013',
            'positions' : positions } )

def faculty(request):
    faculty = Faculty.objects.all()
    facultyByDept = {}
    for f in faculty:
        facultyByDept.setdefault(str(f.get_dept_display()), []).append(
                (f.name, f.chapter, f.graduation, f.link))
    facultyByDept['Advisors'] = [
            ('William R. Goodin', 'CA E', "'75 (Chief Advisor)", ''),
            ('Stacey Ross', 'CA K', "'06 (District 16 Director)", ''),
            ('Neal Bussett', 'CA X', "'09 (District 16 Director)", ''),
            ('Jason Corl', 'CA Q', "'06 (District 16 Director)", ''),
            ('Scott Eckersall', 'CA I', "'96 (District 16 Director)", '')
            ]
    facultyByDept = [(dept, facultyByDept[dept]) for dept in sorted(facultyByDept)]
    return render_next(request, 'faculty.html', {
            'faculty' : facultyByDept,
            'facultyAdvisor' : 'Ann R. Karagozian'
        })

def contact(request):
    return render_next(request, 'contact.html')

def eligibility_list(request):
    return render_next(request, 'eligibility_list.html')

def feedback(request):
    if request.method == "POST" and 'comment' in request.POST:
        Feedback(comment=request.POST.get('comment')).save()
    return redirect('main.views.tutoring')

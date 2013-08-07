from web.views import render_next
from tutoring.models import Tutoring, Class
from main.models import Current

def schedule(request):
    term = Current.objects.get_term()
    tutoring = Tutoring.objects.filter(term=term)
    tutors = []
    for hour, hour_name in Tutoring.HOUR_CHOICES:
        tutors.append([hour_name])
        tutors_for_hour = []
        for day, day_name in Tutoring.DAY_CHOICES:
            tutors_for_hour.append(
            list(tutoring.filter(hour_1=hour, day_1=day)) +
            list(tutoring.filter(hour_2=hour, day_2=day)))
        tutors[-1].append(tutors_for_hour)
    classes = []
    for department, null in Class.DEPT_CHOICES:
        classes.append([department])
        classes[-1].append([(c.course_number, c.department+c.course_number)
        for c in Class.objects.filter(department=department)])
            
    return render_next(request, 'schedule.html', 
            {'classes': classes, 'tutors': tutors})


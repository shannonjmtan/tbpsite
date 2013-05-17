from web.views import render_next

def schedule(request):
    return render_next(request, 'tutoring_schedule.html')


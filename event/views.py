from event.models import Event
from web.views import render_next
from datetime import datetime

def events(request): 
    today = datetime.today()
    return render_next(request, 'events.html', 
            {'upcoming_events': Event.objects.filter(end__gt=today),
                'past_events': Event.objects.filter(end__lte=today)})

def event(request, url):
    return render_next(request, 'event_template.html', 
            {'event': Event.objects.get(url=url)})

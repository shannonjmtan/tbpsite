from event.models import Event
from web.views import render_next
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import Http404

def events(request): 
    today = datetime.today()
    return render_next(request, 'events.html', 
            {'upcoming_events': Event.objects.filter(end__gt=today),
                'past_events': Event.objects.filter(end__lte=today)})

def event(request, url):
    try:
        event = Event.objects.get(url=url)
    except ObjectDoesNotExist:
        raise Http404
    return render_next(request, 'event_template.html', 
            {'event': Event.objects.get(url=url)})

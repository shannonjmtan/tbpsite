from event.models import Event
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, Http404
from common import render

def events(request): 
    today = datetime.today()
    return render(request, 'events.html', 
            {'upcoming_events': Event.objects.filter(end__gt=today),
                'past_events': Event.objects.filter(end__lte=today)})

def event(request, url):
    try:
        event = Event.objects.get(url=url)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'event_template.html', 
            {'event': Event.objects.get(url=url)})

def event_redirect(request, event_url):
    return redirect('/events/' + event_url)

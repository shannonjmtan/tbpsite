#!/usr/bin/env python

from django.shortcuts import render as django_render
from event.models import Event

def render(request, template_name, additional=None):
    dictionary = {'user': request.user, 'next': request.path, 
            'events': Event.objects.filter(dropdown=True)}
    if additional is not None:
        dictionary.update(additional)
    return django_render(request, template_name, dictionary)


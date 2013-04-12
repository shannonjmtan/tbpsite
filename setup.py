#!/usr/bin/env python
from django.core.management import setup_environ
from tbpsite import settings
setup_environ(settings)

from main.models import *
term = Term.objects.get_or_create(quarter='1', year=2013)[0]
current = Current.objects.get_or_create(term=term)[0]
for t in House.HOUSE_CHOICES:
    house = House.objects.get_or_create(house=t[0])[0]
    HousePoints(house=house, term=term).save()

#!/usr/bin/env python
from django.core.management import setup_environ
from tbpsite import settings
setup_environ(settings)

from app.models import House
for t in House.HOUSE_CHOICES:
    House(house=t[0]).save()

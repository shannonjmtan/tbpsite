#!/usr/bin/env python
from django.core.management import setup_environ
from tbpsite import settings
setup_environ(settings)

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from main.models import *
from main.admin import create_candidate
import csv, sys

if len(sys.argv) != 4:
    print('csv quarter year')
    exit()

term = Term.objects.get_or_create(quarter=sys.argv[2], year=sys.argv[3])[0]
print str(term.__unicode__()), 'y/n?',
if raw_input() != 'y':
    exit()

with open(sys.argv[1]) as csvfile:
    csvfile.next()
    for row in csv.reader(csvfile):
        try:
            timestamp, last_name, first_name, _, _, _, _, email, _, expected, major,\
                    = row[:11]
        except ValueError:
            print row
            continue
        
        try:
            user = User.objects.create_user(username=email, email=email)
        except IntegrityError:
            print row
            continue
        user.last_name = last_name
        user.first_name = first_name
        user.save()
        quarter, year = map(int, expected.split('/'))
        graduation_term = Term.objects.get_or_create(quarter=(quarter-1)/3, year=year)[0]
        for t in Profile.MAJOR_CHOICES:
            if t[1] == major:
                major = t[0]
        else:
            major = '0'
        profile = Profile.objects.create(user=user, major=major, initiation_term=term,
                graduation_term=graduation_term)
        create_candidate(profile, term)

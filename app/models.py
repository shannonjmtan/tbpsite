from django.db import models
from django.contrib.auth.models import User

class House(models.Model):
    HOUSE_CHOICES = (
            (0, 'Tau'),
            (1, 'Beta'),
            (2, 'Pi'),
            (3, 'Epsilon'),
            )

    name = models.IntegerField(choices=HOUSE_CHOICES)
                     
    def __unicode__(self):
        return self.name

class Profile(models.Model):
    MAJOR_CHOICES = (
            (0, 'Aerospace Engineering'),
            (1, 'Bioengineering'),
            (2, 'Chemical Engineering'),
            (3, 'Civil Engineering'),
            (4, 'Computer Science'),
            (5, 'Computer Science and Engineering'),
            (6, 'Electrical Engineering'),
            (7, 'Materials Engineering'),
            (8, 'Mechanical Engineering'),
            )
    user = models.ForeignKey(User)
    major = models.IntegerField(choices=MAJOR_CHOICES, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    resume = models.DateTimeField(blank=True, null=True)
    professor_interview = models.DateTimeField(blank=True, null=True)
    house = models.ForeignKey('House', blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()

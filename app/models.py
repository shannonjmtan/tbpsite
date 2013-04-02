from django.db import models
from django.contrib.auth.models import User

class House(models.Model):
    HOUSE_CHOICES = (
            ('Tau', 'Tau'),
            ('Beta', 'Beta'),
            ('Pi', 'Pi'),
            ('Epsilon', 'Epsilon'),
            )

    name = models.CharField(max_length=10, choices=HOUSE_CHOICES)
                     
    def __unicode__(self):
        return self.name

class Profile(models.Model):
    MAJOR_CHOICES = (
            ('Aerospace Engineering', 'Aerospace Engineering'),
            ('Bioengineering', 'Bioengineering'),
            ('Chemical Engineering', 'Chemical Engineering'),
            ('Civil Engineering', 'Civil Engineering'),
            ('Computer Science', 'Computer Science'),
            ('Computer Science and Engineering', 'Computer Science and Engineering'),
            ('Electrical Engineering', 'Electrical Engineering'),
            ('Materials Engineering', 'Materials Engineering'),
            ('Mechanical Engineering', 'Mechanical Engineering'),
            )
    user = models.ForeignKey(User)
    major = models.CharField(max_length=40, choices=MAJOR_CHOICES, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes', blank=True, null=True)
    professor_interview = models.FileField(upload_to='interviews', blank=True, null=True)
    house = models.ForeignKey('House', blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()

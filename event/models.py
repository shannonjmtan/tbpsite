from django.db import models
from main.models import TermManager

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
            ('0', 'Social'),
            ('1', 'Project'),
            ('2', 'Mentorship'),
            ('3', 'House'),
            )

    term = models.ForeignKey('main.Term')
    name = models.CharField(max_length=20)
    descript = models.TextField(max_length=1000)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=80)
    event_type = models.CharField(max_length=1, choices=EVENT_TYPE_CHOICES)
    image = models.ImageField(blank=True, null=True)
    attendees = models.ManyToManyField('main.Profile', blank=True, null=True)

    objects = TermManager()

    class Meta:
        ordering = ('-term', 'name')
        unique_together = ('name', 'term')

    def __unicode__(self):
        return self.name

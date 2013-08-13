from django.db import models
from main.models import TermManager, Settings
import datetime

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
            ('0', 'Social'),
            ('1', 'Project'),
            ('2', 'Mentorship'),
            ('3', 'House'),
            )

    term = models.ForeignKey('main.Term', default=Settings.objects.term)
    name = models.CharField(max_length=40)
    url = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    start = models.DateTimeField()
    end = models.DateTimeField()
    display_time = models.BooleanField(default=True)
    location = models.CharField(max_length=80)
    event_type = models.CharField(max_length=1, choices=EVENT_TYPE_CHOICES)
    image = models.ImageField(upload_to='events', blank=True, null=True)
    dropdown = models.BooleanField()
    attendees = models.ManyToManyField('main.Profile', blank=True, null=True)

    current = TermManager()
    objects = models.Manager()

    class Meta:
        ordering = ('-term', 'name')
        unique_together = ('name', 'term')

    def __unicode__(self):
        return self.name

    def is_same_day(self):
        return self.start.date() == self.end.date()

    def is_upcoming(self):
        return self.end < datetime.datetime.today()

    def get_start(self):
        if self.display_time:
            return self.start.strftime("%a, %m/%d/%y %I:%M%p")
        return self.start.strftime("%a, %m/%d/%y")

    def get_end(self):
        if self.display_time:
            return self.end.strftime("%a, %m/%d/%y %I:%M%p")
        return self.end.strftime("%a, %m/%d/%y")

    def get_date(self):
        return '{}{}'.format(self.start.strftime("%a, %m/%d/%y"), '' if self.is_same_day() else self.end.strftime("-%a, %m/%d/%y"))

    def get_time(self):
        if self.display_time:
            return self.start.strftime("%I:%M%p") + self.end.strftime("-%I:%M%p")
        return ''

    def get_datetime(self):
        return '{}-{}'.format(self.get_start(), self.get_end())

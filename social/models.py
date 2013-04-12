from django.db import models
from main.models import TermManager

class Social(models.Model):
    term = models.ForeignKey('main.Term')
    name = models.CharField(max_length=20)
    attendees = models.ManyToManyField('main.Profile', blank=True, null=True)

    objects = TermManager()

    class Meta:
        ordering = ('-term', 'name')
        unique_together = ('name', 'term')

    def __unicode__(self):
        return self.name

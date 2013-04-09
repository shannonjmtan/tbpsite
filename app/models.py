from django.db import models
from django.contrib.auth.models import User

class CurrentManager(models.Manager):
    def get_queryset(self):
        try:
            return super(CurrentManager, self).get_queryset().get(pk=1)
        except:
            return Current().save()

class Current(models.Model):
    term = models.ForeignKey('Term', blank=True, null=True)
    objects = CurrentManager()

    class Meta:
        verbose_name_plural = "Current"

    def __unicode__(self):
        if self.term is not None:
            return self.term.__unicode__()
        return 'None'

class Term(models.Model):
    QUARTER_CHOICES = (
            ('0', 'Winter'),
            ('1', 'Spring'),
            ('2', 'Summer'),
            ('3', 'Fall'),
            )
    quarter = models.CharField(max_length=1, choices=QUARTER_CHOICES)
    year = models.IntegerField()

    class Meta:
        ordering = ['-year', '-quarter']
        unique_together = ('quarter', 'year')

    def __unicode__(self):
        return self.get_quarter_display() + ' ' + str(self.year)

class House(models.Model):
    HOUSE_CHOICES = (
            ('0', 'Tau'),
            ('1', 'Beta'),
            ('2', 'Pi'),
            ('3', 'Epsilon'),
            )
    house = models.CharField(max_length=1, choices=HOUSE_CHOICES)
                     
    def __unicode__(self):
        return self.get_house_display()

class Profile(models.Model):
    MAJOR_CHOICES = (
            ('0', 'Aerospace Engineering'),
            ('1', 'Bioengineering'),
            ('2', 'Chemical Engineering'),
            ('3', 'Civil Engineering'),
            ('4', 'Computer Science'),
            ('5', 'Computer Science and Engineering'),
            ('6', 'Electrical Engineering'),
            ('7', 'Materials Engineering'),
            ('8', 'Mechanical Engineering'),
            )
    POSITION_CHOICES = (
            ('0', 'Candidate'),
            ('1', 'Member'),
            )
    user = models.ForeignKey(User)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES, default='0')
    house = models.ForeignKey('House', blank=True, null=True)
    major = models.CharField(max_length=1, choices=MAJOR_CHOICES, blank=True)
    initiation_term = models.ForeignKey('Term', related_name='profile_initiation', blank=True, null=True)
    graduation_term = models.ForeignKey('Term', related_name='profile_graduation', blank=True, null=True)
    resume = models.DateTimeField(blank=True, null=True)
    professor_interview = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        ret = self.user.get_full_name()
        if ret:
            return ret
        return self.user.get_username()

class Feedback(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

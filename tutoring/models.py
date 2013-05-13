from django.db import models
from main.models import TermManager

TUTORING_HOURS_PER_WEEK = 2

class Feedback(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

class Tutoring(models.Model):
    profile = models.ForeignKey('main.Profile')
    term = models.ForeignKey('main.Term')

    DAY_CHOICES = (
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            )
    day_1 = models.CharField(max_length=1, choices=DAY_CHOICES, default='0')
    day_2 = models.CharField(max_length=1, choices=DAY_CHOICES, blank=True, null=True)
    week_3 = models.ForeignKey('Week3')
    week_4 = models.ForeignKey('Week4')
    week_5 = models.ForeignKey('Week5')
    week_6 = models.ForeignKey('Week6')
    week_7 = models.ForeignKey('Week7')
    week_8 = models.ForeignKey('Week8')
    week_9 = models.ForeignKey('Week9')

    default = TermManager()

    class Meta:
        ordering = ('-term', 'profile')
        unique_together = ('profile', 'term')
        verbose_name_plural = "Tutoring"

    def __unicode__(self):
        return self.profile.__unicode__()

    def get_weeks(self):
        return [self.week_3, self.week_4, self.week_5, 
                self.week_6, self.week_7, 
                self.week_8, self.week_9]

    def complete(self):
        return all(week.complete() for week in self.get_weeks())

    def points(self):
        return sum(week.points() for week in self.get_weeks())

class Week(models.Model):
    profile = models.ForeignKey('main.Profile')
    term = models.ForeignKey('main.Term')

    hours = models.IntegerField(default=0)
    tutees = models.IntegerField(default=0)

    objects = TermManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.profile.__unicode__()

    def complete(self):
        return self.hours > TUTORING_HOURS_PER_WEEK

    def points(self):
        return 0 if not self.complete() else self.hours - TUTORING_HOURS_PER_WEEK

    def day_1(self):
        return Tutoring.objects.get(profile=self.profile, term=self.term).day_1

    def day_2(self):
        return Tutoring.objects.get(profile=self.profile, term=self.term).day_2

class Week3(Week):
    class Meta:
        verbose_name_plural = "Week 3"

class Week4(Week):
    class Meta:
        verbose_name_plural = "Week 4"

class Week5(Week):
    class Meta:
        verbose_name_plural = "Week 5"

class Week6(Week):
    class Meta:
        verbose_name_plural = "Week 6"

class Week7(Week):
    class Meta:
        verbose_name_plural = "Week 7"

class Week8(Week):
    class Meta:
        verbose_name_plural = "Week 8"

class Week9(Week):
    class Meta:
        verbose_name_plural = "Week 9"

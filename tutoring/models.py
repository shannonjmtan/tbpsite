from django.db import models
from main.models import TermManager

TUTORING_HOURS_PER_WEEK = 2

class Feedback(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

class Class(models.Model):
    DEPT_CHOICES = (
            ('BE', 'BE'),
            ('CEE', 'CEE'),
            ('CHEM', 'CHEM'),
            ('CHEME', 'CHEME'),
            ('CS', 'CS'),
            ('EE', 'EE'),
            ('ENG', 'ENG'),
            ('LS', 'LS'),
            ('MAE', 'MAE'),
            ('MATH', 'MATH'),
            ('MGMT', 'MGMT'),
            ('MSE', 'MSE'),
            ('PHYSICS', 'PHYSICS'),
            ('STATS', 'STATS'),
            )
    department = models.CharField(max_length=10, choices=DEPT_CHOICES)
    course_number = models.CharField(max_length=10)
    display = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Classes"

    def __unicode__(self):
        return self.department + ' ' + self.course_number

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
    HOUR_CHOICES = (
            ('0', '10am'),
            ('1', '11am'),
            ('2', '12pm'),
            ('3', '1pm'),
            ('4', '2pm'),
            ('5', '3pm'),
            ('6', '4pm'),
            )
    day_1 = models.CharField(max_length=1, choices=DAY_CHOICES, default='0')
    hour_1 = models.CharField(max_length=1, choices=HOUR_CHOICES, default='0')
    day_2 = models.CharField(max_length=1, choices=DAY_CHOICES, default='0')
    hour_2 = models.CharField(max_length=1, choices=HOUR_CHOICES, default='0')

    week_3 = models.ForeignKey('Week3')
    week_4 = models.ForeignKey('Week4')
    week_5 = models.ForeignKey('Week5')
    week_6 = models.ForeignKey('Week6')
    week_7 = models.ForeignKey('Week7')
    week_8 = models.ForeignKey('Week8')
    week_9 = models.ForeignKey('Week9')

    objects = TermManager()

    class Meta:
        ordering = ('-term', 'profile')
        unique_together = ('profile', 'term')
        verbose_name_plural = "Tutoring"

    def __unicode__(self):
        return self.profile.__unicode__()

    def classes(self):
        return self.profile.classes

    def get_weeks(self):
        return [self.week_3, self.week_4, self.week_5, self.week_6, self.week_7, self.week_8, self.week_9]

    def complete(self):
        return all(week.complete() for week in self.get_weeks())

    def points(self):
        return sum(week.points() for week in self.get_weeks())

    def get_class_classes(self):
        return ' '.join([c.department+c.course_number+'_1' for c in self.classes().all() if c.display])

    def get_classes(self):
        return ', '.join([c.__unicode__() for c in self.classes().all() if c.display])

class Week(models.Model):
    profile = models.ForeignKey('main.Profile')
    term = models.ForeignKey('main.Term')

    hours = models.IntegerField(default=0)
    tutees = models.IntegerField(default=0)

    objects = TermManager()

    class Meta:
        abstract = True
        ordering = ('tutoring__day_1', 'tutoring__hour_1',
                'tutoring__day_2', 'tutoring__hour_2', 'profile')

    def __unicode__(self):
        return self.profile.__unicode__()

    def complete(self):
        return self.hours >= TUTORING_HOURS_PER_WEEK

    def points(self):
        return (0 if not self.complete() 
                else self.hours - TUTORING_HOURS_PER_WEEK)

    def day_1(self):
        return Tutoring.objects.get(
                profile=self.profile, term=self.term).get_day_1_display()

    def day_2(self):
        return Tutoring.objects.get(
                profile=self.profile, term=self.term).get_day_2_display()

    def hour_1(self):
        return Tutoring.objects.get(
                profile=self.profile, term=self.term).get_hour_1_display()

    def hour_2(self):
        return Tutoring.objects.get(
                profile=self.profile, term=self.term).get_hour_2_display()

class Week3(Week):
    class Meta(Week.Meta):
        verbose_name_plural = "Week 3"

class Week4(Week):
    class Meta(Week.Meta):
        verbose_name_plural = "Week 4"

class Week5(Week):
    class Meta(Week.Meta):
        verbose_name_plural = "Week 5"

class Week6(Week):
    class Meta(Week.Meta):
        verbose_name_plural = "Week 6"

class Week7(Week):
    class Meta(Week.Meta):
        verbose_name_plural = "Week 7"

class Week8(Week):
    class Meta(Week.Meta):
        verbose_name_plural = "Week 8"

class Week9(Week):
    class Meta(Week.Meta):
        verbose_name_plural = "Week 9"

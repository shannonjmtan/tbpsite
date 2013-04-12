from django.db import models
from main.models import TermManager

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

    objects = TermManager()

    class Meta:
        #ordering = ['profile']
        unique_together = ('profile', 'term')
        verbose_name_plural = "Tutoring"

    def __unicode__(self):
        return self.profile.__unicode__()

    def get_hours(self):
        return [self.week_3.hours, self.week_4.hours, self.week_5.hours, 
                self.week_6.hours, self.week_7.hours, 
                self.week_8.hours, self.week_9.hours]

    def complete(self):
        return all(lambda hours: hours >= 2, self.get_hours())

    def points(self):
        return sum(hours - 2 if hours > 2 else 0 for hours in self.get_hours())

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

class Week3(Week):
    class Meta:
        verbose_name_plural = "Week 3"

    def day_1(self):
        return Tutoring.objects.get(week_3=self).day_1

    def day_2(self):
        return Tutoring.objects.get(week_3=self).day_2

class Week4(Week):
    class Meta:
        verbose_name_plural = "Week 4"

    def day_1(self):
        return Tutoring.objects.get(week_4=self).day_1

    def day_2(self):
        return Tutoring.objects.get(week_4=self).day_2

class Week5(Week):
    class Meta:
        verbose_name_plural = "Week 5"

    def day_1(self):
        return Tutoring.objects.get(week_5=self).day_1

    def day_2(self):
        return Tutoring.objects.get(week_5=self).day_2

class Week6(Week):
    class Meta:
        verbose_name_plural = "Week 6"

    def day_1(self):
        return Tutoring.objects.get(week_6=self).day_1

    def day_2(self):
        return Tutoring.objects.get(week_6=self).day_2

class Week7(Week):
    class Meta:
        verbose_name_plural = "Week 7"

    def day_1(self):
        return Tutoring.objects.get(week_7=self).day_1

    def day_2(self):
        return Tutoring.objects.get(week_7=self).day_2

class Week8(Week):
    class Meta:
        verbose_name_plural = "Week 8"

    def day_1(self):
        return Tutoring.objects.get(week_8=self).day_1

    def day_2(self):
        return Tutoring.objects.get(week_8=self).day_2

class Week9(Week):
    class Meta:
        verbose_name_plural = "Week 9"

    def day_1(self):
        return Tutoring.objects.get(week_9=self).day_1

    def day_2(self):
        return Tutoring.objects.get(week_9=self).day_2

from django.db import models
from django.contrib.auth.models import User

PLACE_CHOICES = (
        ('0', 'Not Completed'),
        ('1', 'Completed'),
        ('2', '3rd'),
        ('3', '2nd'),
        ('4', '1st'),
        )
PLACE_POINTS = {
        '0': 0,
        '1': 0,
        '2': 5,
        '3': 10,
        '4': 25,
        }

class CurrentManager(models.Manager):
    def get_term(self):
        queryset = super(CurrentManager, self).get_query_set()
        if not queryset.exists():
            return None
        return queryset[0].term

class TermManager(models.Manager):
    def get_query_set(self):
        term = Current.objects.get_term()
        if term is None:
            return super(TermManager, self).get_query_set()
        return super(TermManager, self).get_query_set().filter(term=term)

class Current(models.Model):
    term = models.ForeignKey('Term', blank=True, null=True)
    objects = CurrentManager()

    class Meta:
        verbose_name_plural = "Current Term"

    def __unicode__(self):
        if self.term is not None:
            return self.term.__unicode__()
        return str(None)

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
    house = models.CharField(max_length=1, choices=HOUSE_CHOICES, unique=True)

    def __unicode__(self):
        return self.get_house_display()

class HousePoints(models.Model):
    house = models.ForeignKey('House')
    term = models.ForeignKey('Term')
    
    professor_interview = models.IntegerField(choices=PLACE_CHOICES, default=0)
    resume = models.IntegerField(choices=PLACE_CHOICES, default=0)
    other = models.IntegerField(default=0)

    objects = TermManager()

    class Meta:
        unique_together = ('house', 'term')
        verbose_name_plural = "House Points"
                     
    def __unicode__(self):
        return self.house.__unicode__()

    def candidate_list(self):
        return Candidate.objects.select_related().filter(profile__house=self.house, 
                profile__initation_term=self.term)

    def candidate_points(self):
        return sum(candidate.points() for candidate in self.candidate_list())

    def points(self):
        return sum([PLACE_POINTS[self.professor_interview], 
                PLACE_CHOICES[self.resume], self.candidate_points()])

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)

    POSITION_CHOICES = (
            ('0', 'Candidate'),
            ('1', 'Member'),
            )
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
    position = models.CharField(max_length=1, choices=POSITION_CHOICES, default='0')
    house = models.ForeignKey('House', blank=True, null=True)
    major = models.CharField(max_length=1, choices=MAJOR_CHOICES, default='0')
    graduation_term = models.ForeignKey('Term', blank=True, null=True)
    resume = models.DateTimeField(blank=True, null=True)
    professor_interview = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        ret = self.user.get_full_name()
        if ret:
            return ret
        return self.user.get_username()

    def initiation_term(self):
        return Candidate.objects.get(profile=self).term

class Candidate(models.Model):
    profile = models.ForeignKey('Profile', unique=True)
    term = models.ForeignKey('Term')

    tutoring = models.ForeignKey('tutoring.Tutoring')
    bent_polish = models.BooleanField(default=False)
    candidate_quiz = models.CharField(max_length=1, choices=PLACE_CHOICES, default='0')
    candidate_meet_and_greet = models.BooleanField(default=False)
    signature_book = models.CharField(max_length=1, choices=PLACE_CHOICES, default='0')
    community_service = models.IntegerField(default=0)
    initiation_fee = models.BooleanField(default=False)
    engineering_futures = models.BooleanField(default=False)
    other = models.IntegerField(default=0)

    objects = TermManager()
    default = models.Manager()

    def __unicode__(self):
        return self.profile.__unicode__()

    #def tutoring(self):
        #return tutoring.complete()

    def tutoring_points(self):
        return self.tutoring.points()

    def social_event_count(self):
        return Social.objects.filter(members=self).count()

    def social_event(self):
        return (self.social_event_count() >= 1)

    def social_event_points(self):
        count = self.social_event_count()
        if count <= 1:
            return 0
        return 5 * count

    def community_service_points(self):
        if self.community_service <= 1:
            return 0
        return 5 * self.community_service

    def points(self):
        return sum([PLACE_POINTS[self.signature_book], 
            PLACE_POINTS[self.candidate_quiz], 
                self.social_event_points(), self.tutoring_points(), 
                self.community_service_points(), self.other])

    def resume(self):
        return self.profile.resume is not None

    def professor_interview(self):
        return self.profile.professor_interview is not None

class ActiveMember(models.Model):
    profile = models.ForeignKey('Profile', unique=True)
    term = models.ForeignKey('Term')

    REQUIREMENT_CHOICES = (
            ('0', 'EMCC'),
            ('1', 'Tutoring'),
            ('2', 'Committee'),
            )
    requirement_choice = models.CharField(max_length=1, choices=REQUIREMENT_CHOICES, default='0')
    requirement_complete = models.BooleanField(default=False)
    tutoring = models.ForeignKey('tutoring.Tutoring', blank=True, null=True)

    objects = TermManager()

    def __unicode__(self):
        return profile.__unicode__()

    class Meta:
        unique_together = ('profile', 'term')

    def requirement(self):
        if not self.requirement_choice:
            return False
        if self.requirement_choice == '0' or self.requirement_choice == '2':
            return requirement_complete
        if tutoring is None:
            return False
        return all(map(lambda hours: hours >= 2, tutoring.get_hours()))

    def social_event(self):
        return (Social.objects.filter(members=self).count() >= 2)

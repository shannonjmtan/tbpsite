from django.db import models
from django.contrib.auth.models import User

CANDIDATE_COMMUNITY_SERVICE = 1
CANDIDATE_SOCIAL = 2
ACTIVE_MEMBER_SOCIAL = 2

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

class CurrentManager(models.Manager):
    def get_term(self):
        queryset = super(CurrentManager, self).get_query_set()
        if not queryset.exists():
            return None
        return queryset[0].term

class Current(models.Model):
    term = models.ForeignKey('Term', blank=True, null=True)
    objects = CurrentManager()

    class Meta:
        verbose_name_plural = "Current Term"

    def __unicode__(self):
        if self.term is not None:
            return self.term.__unicode__()
        return str(None)

class TermManager(models.Manager):
    def get_query_set(self):
        term = Current.objects.get_term()
        if term is None:
            return super(TermManager, self).get_query_set()
        return super(TermManager, self).get_query_set().filter(term=term)

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
    
    resume = models.IntegerField(choices=PLACE_CHOICES, default=0)
    professor_interview = models.IntegerField(choices=PLACE_CHOICES, default=0)
    other = models.IntegerField(default=0)

    objects = TermManager()

    class Meta:
        ordering = ('-term', 'house')
        unique_together = ('house', 'term')
        verbose_name_plural = "House Points"
                     
    def __unicode__(self):
        return self.house.__unicode__()

    def candidate_list(self):
        return Candidate.objects.select_related().filter(
                profile__house=self.house, term=self.term)

    def candidate_points(self):
        return sum(candidate.points() for candidate in self.candidate_list())

    def points(self):
        return sum([PLACE_CHOICES[self.resume], 
            PLACE_POINTS[self.professor_interview], self.candidate_points()])

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)

    CANDIDATE = '0'
    MEMBER = '1'
    POSITION_CHOICES = (
            (CANDIDATE, 'Candidate'),
            (MEMBER, 'Member'),
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
    initiation_term = models.ForeignKey('Term', 
            related_name='profile_initiation_term', default=Current.objects.get_term)
    graduation_term = models.ForeignKey('Term', 
            related_name='profile_graduation_term', blank=True, null=True)
    resume = models.DateTimeField(blank=True, null=True)
    professor_interview = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('position', 'user__last_name', 'user__first_name')

    def __unicode__(self):
        ret = self.user.get_full_name()
        return ret if ret else self.user.get_username()

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

    default = TermManager()
    objects = models.Manager()

    class Meta:
        ordering = ('profile__user__last_name', 'profile__user__first_name')

    def __unicode__(self):
        return self.profile.__unicode__()

    def candidate_quiz_complete(self):
        return self.candidate_quiz != '0'

    def signature_book_complete(self):
        return self.signature_book != '0'

    def tutoring_complete(self):
        return self.tutoring.complete()

    def tutoring_points(self):
        return self.tutoring.points()

    def social_count(self):
        from event.models import Event
        return Event.objects.filter(attendees=self, term=self.term).count()

    def social_complete(self):
        return (self.social_count() >= CANDIDATE_SOCIAL)

    def social_points(self):
        return (0 if not social_complete() else
                5 * (self.social_count() - CANDIDATE_SOCIAL))

    def community_service_complete(self):
        return self.community_service >= CANDIDATE_COMMUNITY_SERVICE

    def community_service_points(self):
        return (0 if not self.community_service_points() else
                5 * (self.community_service - CANDIDATE_COMMUNITY_SERVICE))

    def points(self):
        return sum([PLACE_POINTS[self.signature_book], 
            PLACE_POINTS[self.candidate_quiz], 
                self.social_points(), self.tutoring_points(), 
                self.community_service_points(), self.other])

    def resume(self):
        return self.profile.resume is not None

    def professor_interview(self):
        return self.profile.professor_interview is not None

    def complete(self):
        return (self.tutoring.complete() and self.bent_polish and
                self.candidate_quiz != '0' and self.candidate_meet_and_greet and
                self.signature_book != '0' and self.community_service_complete() and
                self.initiation_fee and self.engineering_futures and
                self.social_complete() and self.resume() and self.professor_interview())

class ActiveMember(models.Model):
    profile = models.ForeignKey('Profile')
    term = models.ForeignKey('Term')

    EMCC = '0'
    TUTORING = '1'
    COMMITTEE = '2'
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
        if self.requirement_choice == EMCC or self.requirement_choice == COMMITTEE:
            return requirement_complete
        if self.tutoring is None:
            self.tutoring = Tutoring.objects.get_or_create(
                    profile=self.profile, term=self.term)[0]
        return self.tutoring.complete()

    def social_complete(self):
        return (Social.objects.filter(members=self).count() >= ACTIVE_MEMBER_SOCIAL)

    def complete(self):
        return self.requirement() and self.social_complete()

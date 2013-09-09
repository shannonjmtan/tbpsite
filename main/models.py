from django.contrib.auth.models import User
from django.db import models

CANDIDATE_COMMUNITY_SERVICE = 1
CANDIDATE_SOCIAL = 2
ACTIVE_MEMBER_SOCIAL = 2

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
DEPT_CHOICES = (
        ('0', 'Bioengineering'),
        ('1', 'Chemical Engineering'),
        ('2', 'Civil and Environmental Engineering'),
        ('3', 'Computer Science'),
        ('4', 'Electrical Engineering'),
        ('5', 'Mechanical and Aerospace Engineering'),
        ('6', 'Materials Science and Engineering') )
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
DAY_CHOICES = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        )
HOUR_CHOICES = (
        ('0', '10am-12pm'),
        ('1', '11am-1pm'),
        ('2', '12pm-2pm'),
        ('3', '1pm-3pm'),
        ('4', '2pm-4pm'),
        ('5', '3pm-5pm'),
        )

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

class SettingsManager(models.Manager):
    def term(self):
        return super(SettingsManager, self).get_or_create(id=1)[0].term

    def display_all_terms(self):
        return super(SettingsManager, self).get_or_create(id=1)[0].display_all_terms

    def display_tutoring(self):
        return super(SettingsManager, self).get_or_create(id=1)[0].display_tutoring

    def get_password(self):
        return super(SettingsManager, self).get_or_create(id=1)[0].registration_password

class Settings(models.Model):
    term = models.ForeignKey('Term', blank=True, null=True)
    display_all_terms = models.BooleanField(default=False)
    display_tutoring = models.BooleanField(default=False)
    registration_password = models.CharField(max_length=10)
    objects = SettingsManager()

    class Meta:
        verbose_name_plural = "Settings"

    def __unicode__(self):
        return 'Settings'

class TermManager(models.Manager):
    def get_query_set(self):
        if not Settings.objects.display_all_terms():
            term = Settings.objects.term()
            if term:
                return super(TermManager, self).get_query_set().filter(term=Settings.objects.term())
        return super(TermManager, self).get_query_set()

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
    
    resume = models.CharField(max_length=1, choices=PLACE_CHOICES, default='0')
    professor_interview = models.CharField(max_length=1, choices=PLACE_CHOICES, default='0')
    signature_book = models.CharField(max_length=1, choices=PLACE_CHOICES, default='0')
    candidate_quiz = models.CharField(max_length=1, choices=PLACE_CHOICES, default='0')
    other = models.IntegerField(default=0)

    objects = TermManager()

    class Meta:
        ordering = ('-term', 'house')
        unique_together = ('house', 'term')
        verbose_name_plural = "House Points"
                     
    def __unicode__(self):
        return self.house.__unicode__()

    def resume_points(self):
        return PLACE_POINTS[self.resume]

    def professor_interview_points(self):
        return PLACE_POINTS[self.professor_interview]

    def signature_book_points(self):
        return PLACE_POINTS[self.signature_book]

    def candidate_quiz_points(self):
        return PLACE_POINTS[self.candidate_quiz]

    def candidate_list(self):
        return Candidate.objects.select_related().filter(profile__house=self.house, term=self.term)

    def social(self):
        return sum(candidate.social_points() for candidate in self.candidate_list())

    def tutoring(self):
        return sum(candidate.tutoring_points() for candidate in self.candidate_list())

    def community_service(self):
        return sum(candidate.community_service_points() for candidate in self.candidate_list())

    def other_points(self):
        return sum(candidate.other for candidate in self.candidate_list()) + self.other

    def points(self):
        return sum([self.resume_points(), self.professor_interview_points(), self.signature_book_points(), self.candidate_quiz_points(),
            self.social(), self.tutoring(), self.community_service(), self.other_points()])

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    middle_name = models.CharField(max_length=30, blank=True)
    nickname = models.CharField(max_length=30, blank=True)
    GENDER_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female'),
            )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=25)

    CANDIDATE = '0'
    MEMBER = '1'
    POSITION_CHOICES = (
            (CANDIDATE, 'Candidate'),
            (MEMBER, 'Member'),
            )
    position = models.CharField(max_length=1, choices=POSITION_CHOICES, default='0')
    house = models.ForeignKey('House', blank=True, null=True)
    major = models.CharField(max_length=1, choices=MAJOR_CHOICES, default='0')
    initiation_term = models.ForeignKey('Term', related_name='profile_initiation_term', default=Settings.objects.term)
    graduation_term = models.ForeignKey('Term', related_name='profile_graduation_term', blank=True, null=True)
    resume_pdf = models.DateTimeField(blank=True, null=True)
    resume_word = models.DateTimeField(blank=True, null=True)
    professor_interview = models.DateTimeField(blank=True, null=True)

    classes = models.ManyToManyField('tutoring.Class', blank=True, null=True)
    day_1 = models.CharField(max_length=1, choices=DAY_CHOICES, default='0')
    hour_1 = models.CharField(max_length=1, choices=HOUR_CHOICES, default='0')
    day_2 = models.CharField(max_length=1, choices=DAY_CHOICES, default='0')
    hour_2 = models.CharField(max_length=1, choices=HOUR_CHOICES, default='2')
    day_3 = models.CharField(max_length=1, choices=DAY_CHOICES, default='0')
    hour_3 = models.CharField(max_length=1, choices=HOUR_CHOICES, default='4')

    class Meta:
        ordering = ('position', 'user__last_name', 'user__first_name')

    def __unicode__(self):
        if self.nickname:
            return '{} {}'.format(self.nickname, self.user.last_name)
        ret = self.user.get_full_name()
        return ret if ret else self.user.get_username()

    def resume(self):
        return self.resume_pdf or self.resume_word

    def dump(self):
        return ','.join(thing for thing in [self.user.first_name, self.middle_name, self.user.last_name, self.user.email, self.nickname, self.gender, 
            self.birthday.strftime('%x') if self.birthday else '', self.phone_number, self.get_major_display(), 
            self.initiation_term.__unicode__() if self.initiation_term else '', self.graduation_term.__unicode__() if self.graduation_term else ''])

class Candidate(models.Model):
    profile = models.ForeignKey('Profile', unique=True)
    term = models.ForeignKey('Term')
    completed = models.BooleanField(default=False)

    tutoring = models.ForeignKey('tutoring.Tutoring')
    bent_polish = models.BooleanField(default=False)
    candidate_quiz = models.BooleanField(default=False)
    candidate_meet_and_greet = models.BooleanField(default=False)
    signature_book = models.BooleanField(default=False)
    community_service = models.IntegerField(default=0)
    initiation_fee = models.BooleanField(default=False)
    engineering_futures = models.BooleanField(default=False)
    other = models.IntegerField(default=0)

    current = TermManager()
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
        return self.profile.resume()

    def professor_interview(self):
        return self.profile.professor_interview is not None

    def requirements(self):
        return (
                ('Tutoring', self.tutoring.complete()),
                ('Bent Polish', self.bent_polish),
                ('Candidate Quiz', self.candidate_quiz),
                ('Signature Book', self.signature_book),
                ('Community Service', self.community_service_complete()),
                ('Initiation Fee', self.initiation_fee),
                ('Engineering Futures', self.engineering_futures),
                ('Social', self.social_complete()),
                ('Resume', self.resume()),
                ('Professor Interview', self.professor_interview())
                )

    def complete(self):
        return all(requirement for name, requirement in self.requirements())

class ActiveMember(models.Model):
    profile = models.ForeignKey('Profile')
    term = models.ForeignKey('Term')
    completed = models.BooleanField(default=False)

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

    current = TermManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.profile.__unicode__()

    class Meta:
        unique_together = ('profile', 'term')
        ordering = ('term',)

    def requirement(self):
        if self.requirement_choice in (ActiveMember.EMCC, ActiveMember.COMMITTEE):
            return self.requirement_complete
        if self.tutoring is None:
            self.tutoring, created = Tutoring.objects.get_or_create(profile=self.profile, term=self.term)
        return self.tutoring.complete()

    def social_complete(self):
        from event.models import Event
        return Event.objects.filter(attendees=self, term=self.term).count() >= ACTIVE_MEMBER_SOCIAL

    def complete(self):
        return self.requirement() and self.social_complete()

class Officer(models.Model):
    position = models.CharField(max_length=30)
    rank = models.IntegerField()
    profile = models.ManyToManyField('Profile')

    def list_profiles( self ):
        return ', '.join( [ str( a ) for a in self.profile.all() ] )

    def __unicode__(self):
        return self.position

    class Meta:
        ordering = ('rank',)

class Faculty(models.Model):
    name = models.CharField(max_length=40)
    dept = models.CharField(max_length=1, choices=DEPT_CHOICES)
    chapter = models.CharField(max_length=10)
    graduation = models.CharField(max_length=10)
    link = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name

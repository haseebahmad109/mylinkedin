from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from permission.tests.test_decorators import test_permission_required


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = datetime.datetime.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.full_name = user.first_name + user.last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_email_verified = models.BooleanField('verified', default=False)
    county_choices = (
        ('Pakistan', 'Pakistan'),
        ('India', 'India'),
        ('Afghanistan', 'Afghanistan')
    )
    country = models.CharField(max_length=1000, choices=county_choices)
    postal_code = models.IntegerField(blank=True, null=True)
    user_type_choices = (
        ('Employed', 'Employed'),
        ('Job Seeker', 'Job Seeker'),
        ('Student', 'Student'),
    )
    user_type = models.CharField(max_length=50, choices=user_type_choices)
    USERNAME_FIELD = 'email'
    date_joined = models.DateTimeField(default=datetime.datetime.now())
    profile_pic = models.ImageField(upload_to="uploads", default="uploads/default_profile.jpg")


    objects = UserManager()

    def get_full_name(self):
        return u' '.join((self.first_name, self.last_name))

    def get_short_name(self):
        return u' '(self.first_name)


class student(models.Model):
    user_id = models.ForeignKey('User')
    School_University = models.CharField(max_length=300, blank=False, null=False)
    DateAttended_from = models.CharField(max_length=5)
    DateAttended_to = models.CharField(max_length=5)
    Age = models.CharField(max_length=10, default='18+')
    Date_of_Birth = models.CharField(max_length=50, blank=True, null=True)


class jobSeeker(models.Model):
    user_id = models.ForeignKey('User')
    most_recent_job_title = models.CharField(max_length=1000)
    self_employed = models.BooleanField()
    MostRecentCompany = models.CharField(max_length=1000, blank=True, null=True)
    Industry_choices = (
        ('', '-'),
        ('Accounting', 'Accounting'),
        ('Animation', 'Animation'),
    )
    time_period_choices1 = (
        ('', '-'),
        ('2013', '2013'),
        ('2012', '2012'),
        ('2011', '2011'),
        ('2010', '2010'),
    )
    time_period_choices2 = (
        ('', '-'),
        ('present', 'present'),
        ('2013', '2013'),
        ('2012', '2012'),
        ('2011', '2011'),
        ('2010', '2010'),
    )
    time_period_choices3 = (
        ('', '-'),
        ('2020', '2020'),
        ('2019', '2019'),
        ('2018', '2018'),
        ('2017', '2017'),
        ('2016', '2016'),
    )

    Industry = models.CharField(choices=Industry_choices, max_length=1000)
    TimePeriod_to = models.CharField(max_length=200, choices=time_period_choices1)
    TimePeriod_from = models.CharField(max_length=200, choices=time_period_choices2)


class employed(models.Model):
    user_id = models.ForeignKey('User')
    Job_title = models.CharField(max_length=1000)
    self_employed = models.BooleanField()
    Industry = models.CharField(choices=jobSeeker.Industry_choices, max_length=1000)
    Company = models.CharField(max_length=1000)


class Invitations(models.Model):
    sender_id = models.ForeignKey('User',  related_name='invitation_sender_id')
    receiver_id = models.ForeignKey('User',  related_name='invitation_receiver_id')
    invitation_message = models.TextField()
    relationship_choices = (('colleague', 'colleague'),
                            ('classmate', 'classmate'),
                            ('business partner', 'business partner'),
                            ('friend', 'friend'),
                            ('other', 'other'),
                            ("don't know", "don't know"),
                            )
    relationship_type = models.CharField(max_length=50, choices=relationship_choices)


class Connection(models.Model):
    of_whom = models.ForeignKey('User', related_name='ofWhome')
    with_whom = models.ForeignKey('User', related_name='withWhome')
    related_how = models.CharField(max_length=50, choices=Invitations.relationship_choices)


class Notifications(models.Model):
    of_whom = models.ForeignKey('User')
    type = models.CharField(max_length=1000)
    viewed_status = models.BooleanField(default=False)
    description = models.TextField()


class Message(models.Model):
    of_whom = models.ForeignKey('User', related_name="of_whom")
    to = models.ForeignKey('User', related_name='to')
    subject = models.CharField(max_length=1000)
    body = models.TextField()
    viewed_status = models.BooleanField(default=False)


class Status(models.Model):
    of_whom = models.ForeignKey('User')
    simple_text = models.TextField(blank=True)
    attached_image = models.ImageField(upload_to="uploads", blank=True)
    link = models.CharField(max_length=200, blank=True)
    link_subject = models.CharField(max_length=1000, blank=True)
    link_description = models.TextField(blank=True)
    share_type = models.CharField(max_length=100, choices={('public', 'public'), ('connections', 'connections')})
    posted_when = models.DateTimeField(auto_now_add=True, blank=True)


class Comment(models.Model):
    comment_of = models.ForeignKey('Status')
    of_whom = models.ForeignKey('User')
    comment_text = models.TextField()


class Like(models.Model):
    on_which_status = models.ForeignKey('Status')
    of_which_user = models.ForeignKey('User')


class Forgot_Pass(models.Model):
    user_id = models.ForeignKey('User')
    key = models.IntegerField()
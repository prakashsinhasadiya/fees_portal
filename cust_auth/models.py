from django.db import models
from model_utils.models import TimeStampedModel
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
# import uuid


class InstituteRecord(TimeStampedModel):

    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='picture')
    email = models.EmailField(max_length=70, blank=True)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17)
    brochure = models.FileField(upload_to='picture')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class InstituteBranch(TimeStampedModel):

    institute_name = models.ForeignKey(
        InstituteRecord, on_delete=models.CASCADE, related_name='branch_institute')
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='picture')
    email = models.EmailField(max_length=70, blank=True)
    address = models.CharField(max_length=70)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17)
    brochure = models.FileField(upload_to='picture')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class InstituteFees(TimeStampedModel):

    class Meta:
        unique_together = ("fees_type", "branch")

    branch = models.ForeignKey(
        InstituteBranch, on_delete=models.CASCADE, related_name='fees_branch')
    fees_type = models.CharField(max_length=20)
    amount = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.fees_type

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class StudentProfile(TimeStampedModel):

    class Meta:
        unique_together = ("enrollment", "branch")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17)
    enrollment = models.CharField(max_length=30)
    branch = models.ForeignKey(
        InstituteBranch, on_delete=models.CASCADE, related_name='student_branch', null=True)

    COURSE_CHOICES = ((
        ('be', 'B-TECH'),
        ('mba', 'MBA'),
        ('pharmacy', 'PHARMACY'),
    ))

    course = models.CharField(
        max_length=8, choices=COURSE_CHOICES, default='be')
    dob = models.DateField(null=True)

    GENDER_CHOICES = ((
        ('male', 'MALE'),
        ('female', 'FEMALE'),
    ))

    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, default='male')

    address = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class PasswordResetTokens(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField(
        "Tocken ID", max_length=60, null=False, blank=False)


class FeesTransactionDetails(TimeStampedModel):

    # u_id = models.UUIDField(default=uuid.uuid4,editable=False)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='student_transacction')
    amount = models.FloatField(null=True)
    status = models.CharField(max_length=20)
    payment_fees_type = models.ForeignKey(
        InstituteFees, on_delete=models.CASCADE, null=True, related_name='payment_dode_fees_type')
    payment_id = models.CharField(max_length=200)
    payer_id = models.CharField(max_length=200)
    payment_response = JSONField()


@receiver(post_save, sender=InstituteBranch)
def save_institutebranch(sender, instance, **kwargs):
    import pdb
    pdb.set_trace()

    institute = InstituteRecord.objects.get(id=instance.institute_name_id)
    message = render_to_string('user_registrations/branch_craete_email.html', {
                'user': institute,
                'instance':instance
            })
    res = send_mail('Branch Crated', message, settings.FROM_EMAIL, [
                            institute.email], fail_silently=False)



class ImageQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.img.delete()
        super(ImageQuerySet, self).delete(*args, **kwargs)

class Image(models.Model):
    objects = ImageQuerySet.as_manager()
    img = models.ImageField(upload_to=get_image_path)
    ...
    def delete(self, *args, **kwargs):
        self.img.delete()
        super(Image, self).delete(*args, **kwargs)
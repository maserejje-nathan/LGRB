from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from config.choices import roles, legalStatus, citizenship, sex


class MyAccountManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, phone_number, District, County, Subcounty, Parish, Village,
                    legalStatus=legalStatus, image='default', role='client', password=True):

        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Please tell us your first name')
        if not last_name:
            raise ValueError('Please tell us your last name')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            phone_number=phone_number.title(),

            District=District,
            County=County,
            Subcounty=Subcounty,
            Parish=Parish,
            Village=Village,
            password=password,
        )
        user.image = image
        user.legalStatus = legalStatus
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, District, County, Subcounty, Parish, Village,
                         image='default', role='admin', password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            phone_number=phone_number,
            District=District,
            County=County,
            Subcounty=Subcounty,
            Parish=Parish,
            Village=Village,
            password=password,
        )

        user.image = image
        user.role = role
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Otp():
    otp = models.CharField(max_length=200, null=True, blank=True, )
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True, default='NITA')
    last_name = models.CharField(max_length=200, null=True, blank=True, default='Uganda')
    card_number = models.CharField(max_length=9, null=True, blank=True)
    District = models.CharField(max_length=30, null=True, blank=True)
    County = models.CharField(max_length=30, null=True, blank=True)
    Subcounty = models.CharField(max_length=30, null=True, blank=True)
    Parish = models.CharField(max_length=30, null=True, blank=True)
    Village = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sex = models.CharField(max_length=200, choices=sex, null=False, blank=False, default='Male')
    image = models.ImageField(upload_to='media/files', null=True, blank=True, default='default')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=200, choices=roles, null=False, blank=False, default='client')
    legalStatus = models.CharField(max_length=200, choices=legalStatus, null=True, blank=True, default='Company')
    citizenship = models.CharField(max_length=200, choices=citizenship, null=True, blank=True, default="Ugandan")
    brn = models.CharField(max_length=200, null=True, blank=True)
    nin = models.CharField(max_length=14, null=True, blank=True)
    ppn = models.CharField(max_length=14, null=True, blank=True)
    wpn = models.CharField(max_length=14, null=True, blank=True)
    business_registration_date = models.CharField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'phone_number',
        'District',
        'County',
        'Subcounty',
        'Parish',
        'Village'
    ]

    objects = MyAccountManager()

    def __str__(self):
        # first, *middle, last = str(self.first_name).split()
        return f"{self.role} {self.first_name} {self.last_name} "

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def get_full_names(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

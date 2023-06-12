from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings
from config.choices import *


# Create your models here.
class BankGuarantee(models.Model):
    principle_licence_certificate_number = models.CharField( max_length=50, null=False, blank=False)
    Name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True) 
    bank = models.CharField(max_length=70, null=True, blank=True)
    bank_guarantee = models.FileField(default="",upload_to='media/files', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    date_created = models.DateField(null=False, blank=False, auto_now=True)
    
    # verification officer
    verification_authority_status = models.CharField(max_length=30,choices=bank_guarantee_verification_choices, null=True, blank=True)
    verification_authority_remarks = models.TextField(max_length=30, null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, blank=True, on_delete=models.SET_NULL, null=True)
    # forward_for_approval = models.BooleanField(default=False)
    date_verified = models.DateTimeField(null=True, blank=True, auto_now_add=True)


    # approving officer 
    approving_authority_status = models.CharField(max_length=30,choices=bank_guarantee_approved_choices, null=True, blank=True, default=None)
    verification_authority_remarks = models.TextField(max_length=30, null=True, blank=True)
    approved = models.BooleanField(default=False)
    approving_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    # date_approved = models.DateField(null=True, blank=True, auto_now_add=True,)


    def __str__(self):
        return self.Name

    # def get_absolutee_url(self, *args, **kwargs):
    #     return reverse('renewal:bankguarantee-detail', kwargs={'pk':self.pk})


    class  Meta:
        db_table = 'Bank Guarantee '
        managed = True
        verbose_name = 'Bank Guarantee'
        verbose_name_plural = 'Bank Guarantees'


class RenewalBankGuarantee(models.Model):
    rinciple_licence_certificate_number = models.CharField( max_length=50, null=False, blank=False)
    Name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True) 
    bank = models.CharField(max_length=70, null=True, blank=True)
    bank_guarantee = models.FileField(default="",upload_to='media/files', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    date_created = models.DateField(null=False, blank=False,auto_created=True)
    
    def __str__(self):
        return self.Name

    class  Meta:
        db_table = 'Renewal Bank Guarantee '
        managed = True
        verbose_name = 'Renewal Bank Guarantee'
        verbose_name_plural = 'Renewal Bank Guarantees'

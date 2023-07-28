from django.db import models
from config.choices import *
from config.utils import *
from django.conf import settings


'''
class Certificate(models.Model):
    certificateid = models.CharField(max_length=200, primary_key=True, default=certificate_generator(prefix='CERT'), editable=False)
    
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates", default=1)
    title = models.CharField(max_length=50, null=True, blank=True)
    practitioner = models.CharField(max_length=30, null=True, blank=True)
    tin = models.IntegerField(null=True, blank=True)  
    organisation_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    
    # location
    district = models.CharField(max_length=40, null=True, blank=True) 
    city = models.CharField(max_length=40, null=True, blank=True) 
    county = models.CharField(max_length=40, null=True, blank=True) 
    sub_county = models.CharField(max_length=40, null=True, blank=True) 
    village = models.CharField(max_length=40, null=True, blank=True) 

    date_applied = models.DateTimeField(auto_now=True)
    
 

    class Meta:
        db_table = 'Practitioner'
        managed = True
        verbose_name = 'Practitioner'
        verbose_name_plural = 'Practitioners'

    def __str__(self):
        return self.certificate_type 


class Education(models.Model):
    educationid = models.CharField(max_length=200, primary_key=True, default=certificate_generator(prefix='EDUC'), editable=False)
    
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="educations", default=1)
    
    education_level = models.CharField(choices=EDUCATION, max_length=40, null=True, blank=True) 
    institution = models.CharField(max_length=40, null=True, blank=True) 
    location = models.CharField(max_length=40, null=True, blank=True)
    start_date = models.DateField(max_length=40, null=True, blank=True) 
    end_data = models.DateField(max_length=40, null=True, blank=True) 
    award = models.CharField(max_length=40, null=True, blank=True) 
    attachment = models.FileField(upload_to="media", max_length=40, null=True, blank=True)
    date_created = models.DateField()


    class Meta:
        db_table = 'Education'
        managed = True
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'

    def __str__(self):
        return self.institution 


class Experience(models.Model):
    experienceid = models.CharField(max_length=200, primary_key=True, default=certificate_generator(prefix='EXP'), editable=False)
    
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="experiences", default=1)

    start_date = models.DateField()
    end_date = models.DateField()
    responsibilities = models.TextField(max_length=50, null=True, blank=True)
    organisation = models.CharField(max_length=30, null=True, blank=True)
    orgnaisation_address = models.CharField(max_length=50, null=True, blank=True)
    attach_proof = models.CharField(max_length=30, null=True, blank=True)

    
    def __str__(self):
        return self.organisation


    class Meta:
        db_table = 'Work Experience'
        managed = True
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'


class Report(models.Model):
    reportid = models.CharField(max_length=200, primary_key=True, default=certificate_generator(prefix='REPT'), editable=False)
    
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports", default=1)
    document_title = models.CharField(max_length=20, null=True, blank=True)
    document_type = models.CharField(max_length=50, null=True, blank=True)
    developed_by = models.CharField(max_length=30, null=True, blank=True)
    document = models.FileField(upload_to=upload_location, null=True, blank=True)
    date_submitted = models.DateTimeField()
    

    class Meta:
        db_table = 'Report Table'
        managed = True
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        return self.document_title 

'''
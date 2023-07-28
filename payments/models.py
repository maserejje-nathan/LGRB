from django.db import models
from django.conf import settings



class ApplicationFeePayments(models.Model):
    
    application_fee =  models.IntegerField(null=True, blank=True)
    generate_prn =  models.BooleanField(default=False)
    tin = models.IntegerField(null=True, blank=True) 
    prn = models.IntegerField( null=True, blank=True)
    error_code = models.CharField(max_length=30, null=True, blank=True)
    error_desc = models.CharField(max_length=30, null=True, blank=True)
    search_code = models.CharField(max_length=30, null=True, blank=True)
    payment_status = models.CharField(max_length=30, null=True, blank=True)
    payment_description = models.CharField(max_length=30, null=True, blank=True)
    payment_expiry_date = models.CharField(max_length=30, null=True, default="", blank=True)
    payment_registered_on = models.CharField(max_length=30, null=True, blank=True)
    payment_made_by = models.CharField(max_length=30, null=True, blank=True) 
    payment_made_on = models.CharField(max_length=30, null=True, blank=True) 
    

class LicenceFeePayments(models.Model):

    licence_fee =  models.IntegerField(null=True, blank=True)
    generate_prn_licence_fee =  models.BooleanField(default=False)
    
    licence_fee_tin = models.IntegerField(null=True, blank=True) 
    licence_fee_prn = models.IntegerField( null=True, blank=True)
    licence_fee_error_code = models.CharField(max_length=30, null=True, blank=True)
    licence_fee_error_desc = models.CharField(max_length=30, null=True, blank=True)
    licence_fee_search_code = models.CharField(max_length=30, null=True, blank=True)
    
    payment_status = models.CharField(max_length=30, null=True, blank=True)
    payment_description = models.CharField(max_length=30, null=True, blank=True)
    payment_expiry_date = models.CharField(max_length=30, null=True, blank=True)
    payment_registered_on = models.CharField(max_length=30, null=True, blank=True)
    payment_made_by = models.CharField(max_length=30, null=True, blank=True) 
    payment_made_on = models.CharField(max_length=30, null=True, blank=True) 
   
    
class PremisePayment(models.Model):
    
    licence_type = models.CharField(max_length=200, blank=True, null=True, default=" Premise Licence")
    name_of_the_company = models.CharField(max_length=200, null=True, blank=True)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="applicant")
    email = models.CharField(max_length=50, null=True, blank=True)
    premise = models.FileField(upload_to="media/premise", null=True, blank=True)
    tin = models.IntegerField(null=True, blank=True)
    licence_fee = models.IntegerField(null=True, blank=True)
    number_of_premises = models.IntegerField(null=True, blank=True)
    date_applied = models.DateField(blank=True, null=True, auto_now_add=True)
    # ura 
    generate_prn =  models.BooleanField(default=False)
    tin = models.IntegerField(null=True, blank=True) 
    prn = models.IntegerField( null=True, blank=True)
    error_code = models.CharField(max_length=30, null=True, blank=True)
    error_desc = models.CharField(max_length=30, null=True, blank=True)
    search_code = models.CharField(max_length=30, null=True, blank=True)
    payment_status = models.CharField(max_length=30, null=True, blank=True)
    payment_description = models.CharField(max_length=30, null=True, blank=True)
    payment_expiry_date = models.CharField(max_length=30, null=True, blank=True)
    payment_registered_on = models.CharField(max_length=30, null=True, blank=True)
    payment_made_by = models.CharField(max_length=30, null=True, blank=True) 
    payment_made_on = models.CharField(max_length=30, null=True, blank=True) 
    ura_district = models.CharField(max_length=50, null=True, blank=True)
    ura_county =  models.CharField(max_length=50, null=True, blank=True)
    ura_subcounty = models.CharField(max_length=50, null=True, blank=True)
    ura_village = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Premise Payment Table'
        managed = True
        verbose_name = 'Premises Payment'
        verbose_name_plural = 'Premises Payments'
        
    def __str__(self):
        return self.email 


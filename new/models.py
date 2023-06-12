
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver

from config.choices import *
from payments.models import *
from bankguarantee.models import *

import random 
import string

class PrincipleLicence(models.Model):

    licence_type = models.CharField(max_length=100, choices=licence,   blank=True, null=True)
    purpose_of_application =  models.CharField(max_length=100, choices=purpose,   blank=True, null=True)
    previous_licence_number = models.CharField(max_length=100,   blank=True, null=True)
    certificate_number = models.CharField(max_length=200, null=True, blank=True)
    name_of_the_company = models.CharField(max_length=50, null=True, blank=True)
    company_status = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    Address = models.TextField(max_length=300, null=True, blank=True)
    county = models.CharField(max_length=30, null=True, blank=True)
    sub_county = models.CharField(max_length=30, null=True, blank=True)
    parish = models.CharField(max_length=30, null=True, blank=True)
    village = models.CharField(max_length=30, null=True, blank=True)
    plot_number = models.CharField(max_length=50, null=True, blank=True)
    application_fee = models.IntegerField(null=True, blank=True)
    licence_fee =  models.IntegerField(null=True, blank=True)
    projected_gross_turnover = models.TextField( null=True, blank=True, default="")
    previous_business_engagement = models.CharField(max_length=3, choices=BOOL_CHOICE, null=True, blank=True, default="No")
    name_of_the_business = models.CharField(max_length=30, null=True, blank=True, default="")
    engagement_capacity = models.CharField(max_length=30, null=True, blank=True, default="")
    start_date = models.DateField(blank=True, null=True, )
    end_date = models.DateField(blank=True, null=True)
    crime_engagement = models.CharField(max_length=30, choices=BOOL_CHOICE, blank=True, null=True)
    crime_details = models.CharField(max_length=30, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applied_by', default=1, blank=True, on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    tin = models.IntegerField(null=True, blank=True) 

    # Documents 
    bank_guarantee = models.ForeignKey(BankGuarantee,  null=True, blank=True, on_delete=models.CASCADE, related_name='principlelicence_bank_guarantee')
    memorandum_and_articles_of_association = models.FileField(default="",upload_to='media/files/memorandum_and_articles_of_association', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    districts_of_conduction = models.FileField(default="",upload_to='media/files', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    annual_company_returns = models.FileField(default="",upload_to='media/files/annual_company_returns', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    tenancy_agreement = models.FileField( default="",upload_to='media/files/tenacy_agreements', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    categories_of_machines = models.FileField( default="",upload_to='media/files/categories_of_machines', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    class_of_the_casino_games = models.CharField(max_length=50, null=True, blank=True)
    purpose_of_the_lottery  = models.CharField(max_length=50, null=True, blank=True)
    
    applicationfeepayments = models.ForeignKey(ApplicationFeePayments, on_delete=models.CASCADE, related_name='ApplicationFeePayments', null=True, blank=True)
    licencefeepayments = models.ForeignKey(LicenceFeePayments, on_delete=models.CASCADE,  related_name='LicenceFeePayments', null=True,blank=True)

    ura_district = models.CharField(max_length=50, null=True, blank=True)
    ura_county =  models.CharField(max_length=50, null=True, blank=True)
    ura_subcounty = models.CharField(max_length=50, null=True, blank=True)
    ura_village = models.CharField(max_length=50, null=True, blank=True)

    # inspecting officer
    inspection_authority_status = models.CharField(max_length=30, choices=inspection_choices, null=True, blank=True)
    inspection_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    inspected_by = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,  related_name='inspected_by', blank=True, on_delete=models.SET_NULL, null=True)
    forward_for_verification = models.BooleanField(default=False)
    inspection_report  = models.FileField(default="",upload_to='media/files/evaluation_checklist', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    defer_to_inspector = models.BooleanField(default=False)
    date_inspected = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="Date Inspected")
  
    # verification officer
    verification_authority_status = models.CharField(max_length=30,choices=verification_choices, null=True, blank=True)
    verification_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,  related_name='verified_by', blank=True, on_delete=models.SET_NULL, null=True)
    forward_for_approval = models.BooleanField(default=False)
    defer_to_verifier = models.BooleanField(default=False)
    date_verified = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="Date Verified")

    # assigning officer  
    assigned_to_inspector = models.ForeignKey(settings.AUTH_USER_MODEL,  limit_choices_to={'role': 'inspector'}, related_name='assigned_to', blank=True, on_delete=models.SET_NULL, null=True)
    manager_remarks = models.TextField(max_length=30, null=True, blank=True)
    date_assigned = models.DateField(null=True, blank=True,  verbose_name="Date assigned")
    assigned = models.BooleanField(default=False)


    # approving officer 
    approving_authority_status = models.CharField(max_length=30,choices=approved_choices, null=True, blank=True, default=None)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='approved_by', blank=True, on_delete=models.SET_NULL, null=True)
    approving_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    approved = models.BooleanField(default=False)
    date_approved = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name="Date Approved")
   
    date_applied = models.DateField(verbose_name="principle_date_applied", auto_now_add=True, null=True, blank=True)
    expiry_date = models.CharField(max_length=30, null=True, blank=True)
    validity = models.CharField(max_length=30, choices=validity,  verbose_name="premise_licence_validity", null=True, blank=True)

    class Meta:
        db_table = 'Principle Licence'
        managed = True
        verbose_name = 'Principle Licence'
        verbose_name_plural = 'Principle  Licences'

    # def save(self, *args, **kwargs):
    #     # calculate the expiry date
    #     self.expiry_date = self.date_approved + datetime.timedelta(days=365)
    #     super().save(*args, **kwargs)

    # def update_expiry_date(self):
    #     # calculate the expiry date
    #     self.expiry_date = self.date_approved + datetime.timedelta(days=365)
    #     self.save()
   
    def __str__(self):
        return self.name_of_the_company
    
        # return self.date.strftime("%Y %B %d")

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('new:principle-detail', kwargs= {'id': self.id} )

    def get_prn_url(self, *args, **kwargs):
        return reverse('new:get_prn', kwargs= {'id': self.id} )

    def get_update_url(self):
        return reverse("new:principle-update", kwargs={
            'id': self.id
        })



def generate_random_string():

    licence =[
        (None, 'Choose an action'),
        ('License to conduct a National Lottery','License to conduct a National Lottery'),
        ('License to conduct a Public Lottery','License to conduct a Public Lottery'),
        ('Casino operating license','Casino operating license'),
        ('Bingo betting license','Bingo betting license'),
        ('Pool betting license','Pool betting license'),
        ('Betting Intermediary operating license','Betting Intermediary operating license'), 
        ('General betting operating license','General betting operating license'),
        ('License to manufacture supply install or adapt gambling or a gambling software operating license','License to manufacture supply install or adapt gambling or a gambling software operating license'),
    ]

    # Generate a random string of 3 uppercase letters
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    nl_prefix = 'NL'
    bi_prefix = 'BI'
    # Generate a random number between 1 and 99
    number = random.randint(1, 99)
    # Generate a random number between 1 and 999
    digits = random.randint(1, 999)
    # Combine the elements into a string
    
    for licence in PrincipleLicence.objects.all():
        if licence.licence_type == "License to conduct a National Lottery":
            return f"{nl_prefix}-{number:02d}-{digits:03d}"
        elif licence.licence_type == "Betting Intermediary operating license":
            return f"{bi_prefix}-{number:02d}-{digits:03d}"
        else:
            return f"{letters}-{number:02d}-{digits:03d}"


def generate_principle_licence_number(instance):
    new_certificate_number = generate_random_string()
    jclass = instance.__class__
    exists = jclass.objects.filter(certificate_number = new_certificate_number).exists()
    if exists:
        return generate_random_string()
    return new_certificate_number 


def pre_save_update_certificate_number(sender, instance, *args, **kwargs):
    if not instance.certificate_number:
        instance.certificate_number = generate_principle_licence_number(instance)

pre_save.connect(pre_save_update_certificate_number, sender=PrincipleLicence)


class EmployeeLicence(models.Model):

    purpose_of_application =  models.CharField(max_length=10, choices=purpose,   blank=True, null=True)
    refrence_number =  models.CharField(max_length=30, blank=True, null=True, default="Employee Reference Number")
    licence_number = models.CharField(max_length=30, blank=True, null=True, default="Employee Licence Number")
    previous_licence_number = models.CharField(max_length=30, blank=True, null=True, default="Previous Employee Licence Number")
    licence_type = models.CharField(max_length=200, blank=True, null=True, default=" Employee Licence")
    tin = models.IntegerField(null=True, blank=True)
    name_of_the_company = models.CharField(max_length=80, blank=True, null=True)
    name_of_the_employee =  models.CharField(max_length=80, blank=True, null=True)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="Employee")
    email = models.CharField(max_length=30, null=True, blank=True)  
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile_phone = models.IntegerField( null=True, blank=True)
    office_phone = models.IntegerField( null=True, blank=True)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    nationality = models.CharField(choices=CITITZENSHIP_TYPE, default="Ugandan", max_length=200, null=True, blank=True)
    national_id = models.FileField(default=None, null=True, blank=True, upload_to='media/national_id', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    passport = models.FileField(default=None, null=True, blank=True, upload_to='media/passport', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    work_permit = models.FileField(default=None, null=True, blank=True, upload_to='media/work_permit', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    country = models.CharField(max_length=200, null=True, blank=True)
    occupation = models.CharField(max_length=200, choices=occupation, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    professional_membership = models.CharField(max_length=30, null=True, blank=True)
    interpoal_clearance = models.FileField(default=None, upload_to='media/interpoal_clearances', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    cv = models.FileField(default=None, upload_to='media/cv', validators=[FileExtensionValidator(allowed_extensions=['pdf'])]  )
    application_fee = models.IntegerField(null=True, blank=True)
    previous_business_engagement = models.CharField(max_length=20, null=True, blank=True)
    name_of_the_employer = models.CharField(max_length=20, null=True, blank=True)
    crime_engagement = models.CharField(max_length=30, choices=BOOL_CHOICE, blank=True, null=True)
    crime_details = models.CharField(max_length=30, null=True, blank=True)    
    
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

    # assigning officer
    assigned_to_inspector = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'inspector'}, related_name='employee_licence_assigned_to_inspector', blank=True, on_delete=models.SET_NULL, null=True)
    manager_remarks = models.TextField(max_length=30, null=True, blank=True)
    date_assigned = models.DateField(null=True, blank=True,  verbose_name="Date assigned")
    assigned = models.BooleanField(default=False)

    # inspecting officer
    inspection_authority_status = models.CharField(max_length=30, choices=inspection_choices, null=True, blank=True)
    inspection_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    inspected_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='employee_inspected_by', blank=True, on_delete=models.SET_NULL, null=True)
    forward_for_verification = models.BooleanField(default=False)
    date_inspected = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="Date Inspected")
    defer_to_inspector = models.BooleanField(default=False)

    # verification officer
    verification_authority_status = models.CharField(max_length=30,choices=verification_choices, null=True, blank=True)
    verification_authority_remarks = models.TextField(max_length=200, null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,  related_name='employee_verified_by', blank=True, on_delete=models.SET_NULL, null=True)
    forward_for_approval = models.BooleanField(default=False)
    date_verified = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="Date Verified")
    defer_to_verifier = models.BooleanField(default=False)

    # approving officer 
    approving_authority_status = models.CharField(max_length=30,choices=approved_choices, null=True, blank=True, default=None)
    approving_authority_remarks = models.TextField(max_length=200, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='employee_approved_by', blank=True, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    date_approved = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name="Date Approved")
    
    date_applied = models.DateField(verbose_name="employee_date_applied", auto_now_add=True, null=True, blank=True)
    expiry_date = models.CharField(max_length=30, null=True, blank=True)
    validity = models.CharField(max_length=30, choices=validity,  verbose_name="premise_licence_validity", null=True, blank=True)

    

    def __repr__(self):
        return self.name_of_the_company

    def get_employee_detail_url(self, *args, **kwargs):
        return reverse('new:employee-detail', kwargs= {'pk': self.pk} )
    
    def get_employee_update_url(self, *args, **kwargs):
        return reverse('new:employee-update', kwargs= {'pk': self.pk} )

    class  Meta:
        db_table = 'Employee Licence'
        managed = True
        verbose_name = 'Employee Licence'
        verbose_name_plural = 'Employee Licences'


class PremiseLicence(models.Model):

    operator_name = models.CharField(max_length=200, null=True, blank=True)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="premise_applicant")
    email = models.CharField(max_length=30, null=True, blank=True)
    trade_name = models.CharField(max_length=30, null=True, blank=True)
    premise_name = models.CharField(max_length=200, null=True, blank=True)
    region = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)  
    municipality =	models.CharField(max_length=200, null=True, blank=True)
    town_council =	models.CharField(max_length=200, null=True, blank=True)
    plot_number = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    building_name =	models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    equipment_in_the_premise = models.CharField(max_length=200, null=True, blank=True)
    number_of_gaming_devices =  models.CharField(max_length=200, null=True, blank=True)
    inspection_fee = models.IntegerField(null=True, blank=True)
    signature = models.ImageField(null=True, blank=True, default=None)
    
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

    # manager officer
    assigned_to_inspector = models.ForeignKey(settings.AUTH_USER_MODEL,  limit_choices_to={'role': 'inspector'}, related_name='premise_licence_assigned_to_inspector', blank=True, on_delete=models.SET_NULL, null=True)
    manager_remarks = models.TextField(max_length=30, null=True, blank=True)
    assigned = models.BooleanField(default=False)
    date_assigned = models.DateField(null=True, blank=True,  verbose_name="Premise Manager Date assigned")

    # inspecting officer
    inspection_authority_status = models.CharField(max_length=30, choices=inspection_choices, null=True, blank=True)
    inspection_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    inspected_by = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,  related_name='Premise_inspected_by', blank=True, on_delete=models.SET_NULL, null=True)
    forward_for_verification = models.BooleanField(default=False)
    date_inspected = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="premise_date_inspected")
    inspection_report = models.FileField(default="",upload_to='media/files/premise_inspection_report', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    defer_to_inspector = models.BooleanField(default=False)

    # verification officer
    verification_authority_status = models.CharField(max_length=30,choices=verification_choices, null=True, blank=True)
    verification_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,  related_name='premise_verified_by', blank=True, on_delete=models.SET_NULL, null=True)
    forward_for_approval = models.BooleanField(default=False)
    date_verified = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="premise_date Verified")
    defer_to_verifier = models.BooleanField(default=False)

    # approving officer 
    approving_authority_status = models.CharField(max_length=30,choices=approved_choices, null=True, blank=True, default=None)
    approving_authority_remarks = models.TextField(max_length=2000, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='premise_approved_by', blank=True, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    date_approved = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name="premise_date_approved")


    # general checklist 
    licence_availability = models.CharField(max_length=30,choices=AVAILABLE_CHOICE,  null=True, blank=True)
    licence_availability_comments = models.CharField(max_length=30, null=True, blank=True)

    licence_display = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    licence_display_comments = models.CharField(max_length=30, null=True, blank=True)
    
    premises_surrounding_public_amenities = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    premises_urrounding_public_amenities_comments = models.CharField(max_length=30, null=True, blank=True)
     
    convinience_facility = models.CharField(max_length=30, choices=AVAILABLE_CHOICE, null=True, blank=True)
    common_area = models.CharField(max_length=30, choices=AVAILABLE_CHOICE, null=True, blank=True)
    convenience_facilities_and_common_area_comments = models.CharField(max_length=30, null=True, blank=True)

    size_of_premises  = models.CharField(max_length=30, null=True, blank=True)
    size_of_premises_comments = models.CharField(max_length=30, null=True, blank=True)
    
    metal_detector = models.CharField(max_length=30,  choices=AVAILABLE_CHOICE, null=True, blank=True)
    security_guard = models.CharField(max_length=30,  choices=AVAILABLE_CHOICE, null=True, blank=True)
    access_restriction_and_security_comments = models.CharField(max_length=30, null=True, blank=True)

    television_set_positioning = models.CharField(max_length=30, choices=SUITABLE_CHOICE, null=True, blank=True)
    television_set_positioning_comments = models.CharField(max_length=30, null=True, blank=True)
    
    display_of_rules_on_betting_and_gaming = models.CharField(max_length=30, choices=DISPLAY_CHOICE, null=True, blank=True)
    display_of_rules_on_betting_and_gaming_comments = models.CharField(max_length=30, null=True, blank=True)
    
    display_of_board_notices_and_rules =  models.CharField(max_length=30, null=True, choices=DISPLAY_CHOICE, blank=True)
    display_of_board_notices_and_rules_comments = models.CharField(max_length=30, null=True, blank=True)
  
    data_protection_policy = models.CharField(max_length=30, choices=DISPLAY_CHOICE, null=True, blank=True)
    data_protection_policy_comments = models.CharField(max_length=30, null=True, blank=True)

    gaming_tables_number = models.CharField(max_length=30, null=True, blank=True)
    slot_machines_number = models.CharField(max_length=30, null=True, blank=True)
    fish_hunter_number = models.CharField(max_length=30, null=True, blank=True)
    coin_machines_number = models.CharField(max_length=30, null=True, blank=True)

    # cassino and headoffice checklist 
    plans_and_diagram_of_casino = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    plans_and_diagram_of_casino_comments = models.CharField(max_length=30, null=True, blank=True)

    survillance_systems = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    survillance_systems_comments = models.CharField(max_length=30, null=True, blank=True)
    
    counting_rooms_or_cages = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    counting_rooms_or_cages_comments = models.CharField(max_length=30, null=True, blank=True)
    
    casino_and_gaming_rules = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    casino_and_gaming_rules_comments = models.CharField(max_length=30, null=True, blank=True)
    
    communication_facilities = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    communication_facilities_comments = models.CharField(max_length=30, null=True, blank=True)
    
    anti_money_laundering_policy = models.CharField(max_length=30, choices=YESNO_CHOICE, null=True, blank=True)
    anti_money_laundering_policy_comments = models.CharField(max_length=30, null=True, blank=True)


    # general category 
    casino_games = models.CharField(max_length=30, null=True, blank=True)
    slot_machines = models.CharField(max_length=30, null=True, blank=True)
    genera_betting_and_virtual_machines = models.CharField(max_length=30, null=True, blank=True)
    pool_betting = models.CharField(max_length=30, null=True, blank=True)
    bingo_betting = models.CharField(max_length=30, null=True, blank=True)

    date_applied = models.DateField(verbose_name="premise_date_applied", auto_now_add=True, null=True, blank=True)
    expiry_date = models.CharField(max_length=30, verbose_name="premise_date_expired", null=True, blank=True)
    validity = models.CharField(max_length=30,  choices=validity,  verbose_name="premise_licence_validity", null=True, blank=True)

    class Meta:
        db_table = 'Premise Licence Table'
        managed = True
        verbose_name = 'Premise Licence'
        verbose_name_plural = 'Premise Licences'




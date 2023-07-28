from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
from django.db.models.query import QuerySet
import requests

from new.models import *
from django.conf import settings
from django.db import transaction
from config.choices import *
from account.models import *



class PrincipleLicenceForm(forms.ModelForm):
    
    purpose_of_application = forms.ChoiceField(label='Purpose of the application', choices=purpose, required=True, widget=forms.Select(attrs={'class': 'form-control', 'name':'purpose_of_application', 'id':'purpose_of_application','type':'select'}))
    previous_licence_number = forms.CharField(label='Previous licence number', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'previous_licence_number', 'id':'previous_licence_number','type':'text'}))
    licence_type = forms.ChoiceField(label='Select the licence you are applying for ', choices=licence, required=True, widget=forms.Select(attrs={'class': 'form-control licence_type', 'name':'licence_type', 'id':'licence_type','type':'select'}))
    company_status = forms.ChoiceField(label='Select the nature of the company', choices=COMPANY_STATUS, required=True, widget=forms.Select(attrs={'class': 'form-control company_status', 'name':'company_status', 'id':'company_status','type':'select'}))
    email = forms.CharField(label='Email',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'email', 'id':'email','type':'text' }))
    name_of_the_company = forms.CharField(label='Name of the company', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'name_of_the_company', 'id':'name_of_the_company','type':'text'}))
    description = forms.CharField(label='Description', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'description', 'id':'description','type':'text'}))
    district = forms.CharField(label='District', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'district', 'id':'district','type':'text', 'readonly':'readonly'}))
    county = forms.CharField(label='County', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'county', 'id':'county','type':'text', 'readonly':'readonly'}))
    parish = forms.CharField(label='Parish', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'parish', 'id':'parish','type':'text', 'readonly':'readonly'}))
    sub_county = forms.CharField(label='Sub County', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'sub_county', 'id':'sub_county','type':'text', 'readonly':'readonly'}))
    village = forms.CharField(label='Village', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'village', 'id':'village','type':'text', 'readonly':'readonly'}))
    plot_number = forms.CharField(label='Plot Number', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'plot_number', 'id':'plot_number','type':'text'}))
    application_fee = forms.CharField(label='Application Fee', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'application_fee', 'id':'application_fee','type':'text', 'readonly':'readonly'}))
    licence_fee = forms.CharField(label='Licence Fee', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'licence_fee', 'id':'licence_fee','type':'text', 'readonly':'readonly'}))
    projected_gross_turnover = forms.CharField(label='Projected Gross Turnover', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'projected_gross_turnover', 'id':'projected_gross_turnover','type':'text'}))
    previous_business_engagement =  forms.ChoiceField(label='Has the applicant engaged in any gaming ', choices=BOOL_CHOICE, required=True, widget=forms.Select(attrs={'class': 'form-control', 'name':'previous_business_engagement', 'id':'previous_business_engagement','type':'select'}))
    name_of_the_business = forms.CharField(label='Name of the business', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'name_of_the_business', 'id':'name_of_the_business','type':'text'}))
    engagement_capacity = forms.CharField(label='Capacity in which the applicant was engaged', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'engagement_capacity', 'id':'engagement_capacity','type':'text'}))
    start_date = forms.DateField( required=False, widget=forms.DateInput( attrs={ 'id': 'start_date', 'class':'form-control datepicker-input', 'placeholder' : 'dd/mm/yyyy', 'data-datepicker':'' } )   )
    end_date = forms.DateField( required=False, widget=forms.DateInput( attrs={ 'id': 'end_date', 'class':'form-control datepicker-input', 'placeholder' : 'dd/mm/yyyy', 'data-datepicker':'' } )   )
    
    crime_engagement = forms.ChoiceField(label='Has the applicant been convicted for any offence or crime, even though subject of pardon, amnesty, or other similar action', choices=BOOL_CHOICE, required=True, widget=forms.Select(attrs={'class': 'form-control', 'name':'crime_engagement', 'id':'crime_engagement','type':'select'}))
    crime_details = forms.CharField( label='Provide the details of the offence or crime', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'crime_details', 'id':'crime_details','type':'text'}))
   
    form_confirmation = forms.BooleanField( widget=forms.CheckboxInput( attrs={'class': 'form-check-input ', 'name': 'form_confirmation', 'id':'form_confirmation'} ), label = "I certify that the information provided in this application is true and authentic. I am aware that failure to provide accurate information may result into delayed processing or rejection of my application or prosecution in Courts of Law or any other punitive measure for giving misleading information.") 
    tenancy_agreement = forms.FileField(label='Tenancy Agreement ',  required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'tenancy_agreement', 'id':'tenancy_agreement','type':'file' }))
    memorandum_and_articles_of_association = forms.FileField(label='Memorandum and Articles of Assocation',  required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'memorandum_and_articles_of_association', 'id':'memorandum_and_articles_of_association','type':'file' }))
    annual_company_returns = forms.FileField(label='Annual Company Returns',  required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'annual_company_returns', 'id':'annual_company_returns','type':'file' }))
    districts_of_conduction = forms.FileField(label='List of districts where the game is to be conducted',  required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'districts_of_conduction', 'id':'districts_of_conduction','type':'file' }))
    categories_of_machines = forms.FileField(label='Categories of the machines',  required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'categories_of_machines', 'id':'categories_of_machines','type':'file' }))
    purpose_of_the_lottery = forms.CharField( label='Purpose of the lottery ', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'purpose_of_the_lottery', 'id':'purpose_of_the_lottery','type':'text'}))
    class_of_the_casino_games = forms.CharField( label='Class of the casino games', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'class_of_the_casino_games', 'id':'class_of_the_casino_games','type':'text'}))
    tin = forms.CharField(label='TIN of the Company',  required=True, widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'tin', 'id':'tin','type':'text' }))

    # generate_prn = forms.BooleanField(label='Generate Payment Registration Number (PRN)', required=True,  widget=forms.CheckboxInput(attrs={'class': 'form-check-input custom-control-input',  'role':'switch',  'name':'generate_prn', 'id':'generate_prn','type':'checkbox'}))
    # prn = forms.CharField(label='Payment Registration Number(PRN)',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'prn', 'id':'prn','type':'text', 'readonly': 'readonly'}))
    # error_code = forms.CharField(label='error_code',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'error_code', 'id':'error_code','type':'hidden', }))
    # error_desc = forms.CharField(label='error_desc',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'error_desc', 'id':'error_desc','type':'hidden', }))
    # payment_expiry_date = forms.CharField(label='payment_expiry_date',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'payment_expiry_date', 'id':'payment_expiry_date','type':'hidden', }))
    # search_code = forms.CharField(label='search_code',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'search_code', 'id':'search_code','type':'hidden', }))
    ura_district = forms.CharField(label='ura_district',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_district', 'id':'ura_district','type':'text', }))
    ura_county =  forms.CharField(label='ura_county',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_county', 'id':'ura_county','type':'text', }))
    ura_subcounty = forms.CharField(label='ura_subcounty',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_subcounty', 'id':'ura_subcounty','type':'text', }))
    ura_village = forms.CharField(label='ura_village',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_village', 'id':'ura_village','type':'text', }))

    # bingo here 
    # casino here 

    class Meta:
        model = PrincipleLicence
        fields =  '__all__'
        exclude = [
            'applicant',  
            'prn', 
            'error_code' ,
            'error_desc' ,
            'payment_expiry_date',
            'search_code' ,
           
            #  'ura_district',
            # 'ura_county' ,
            # 'ura_subcounty',
            # 'ura_village' ,
        ]


class PrincipleLicenceUpdateForm(forms.ModelForm):

    class Meta:
        model = PrincipleLicence
        fields =  [
            'inspection_authority_status',
            'inspection_authority_remarks',
            'forward_for_verification',
            'inspection_report',
            'defer_to_inspector',

            'verification_authority_status',
            'verification_authority_remarks',
            'forward_for_approval',
            'defer_to_verifier',

            'approving_authority_status',
            'approving_authority_remarks',
            'approved',

            'assigned_to_inspector',
            'manager_remarks', 
            'date_assigned',

        ]
        # fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PrincipleLicenceUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

  
class EmployeeLicenceForm(forms.ModelForm):

    purpose_of_application = forms.ChoiceField(label='Purpose of application ', required=False, choices=purpose,  widget=forms.Select(attrs={'class': 'form-control', 'name':'purpose_of_application', 'id':'purpose_of_application','type':'select'}))
    previous_licence_number =  forms.CharField(label='Enter the previous licence number',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'previous_licence_number', 'id':'previous_licence_number','type':'text'}))
    tin = forms.CharField(label='Enter the Company TIN',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'tin', 'id':'tin','type':'text'}))
    name_of_the_company = forms.CharField(label='Enter the Company Name',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'name_of_the_company', 'id':'name_of_the_company','type':'text', 'readonly':'readonly'}))
    name_of_the_employee = forms.CharField(label='Enter the Employee Name',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'name_of_the_employee', 'id':'name_of_the_employee','type':'text'}))
    address = forms.CharField(label='Address',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'address', 'id':'address','type':'text'}))
    mobile_phone = forms.CharField(min_length=10,  max_length=15, error_messages={'required': 'A valid phone number is required'}, help_text='If in another country, specify the country code e.g. +254', widget=forms.TextInput(attrs={'class': 'form-control', 'name':'mobile_phone', 'id':'mobile_phone','type':'text', 'placeholder':'eg: 0789098975'}))
    office_phone = forms.CharField(min_length=10,  max_length=15, error_messages={'required': 'A valid phone number is required'}, help_text='If in another country, specify the country code e.g. +254', widget=forms.TextInput(attrs={'class': 'form-control', 'name':'office_phone', 'id':'office_phone','type':'text', 'placeholder':'eg: 0789098975'}))
    postal_code = forms.CharField(label='Postal Code',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'postal_code', 'id':'postal_code','type':'text'}))
    nationality = forms.ChoiceField(label='Nationality ', required=False, choices=CITITZENSHIP_TYPE,  widget=forms.Select(attrs={'class': 'form-control', 'name':'nationality', 'id':'nationality','type':'select'}))
    country = forms.CharField(label='Country',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'country', 'id':'country','type':'text'}))
    occupation = forms.ChoiceField(label='Occupation',  choices=occupation, required=True, widget=forms.Select(attrs={'class': 'form-control', 'name':'occupation', 'id':'occupation','type':'text'}))
    
    qualification = forms.CharField(label='Qualification',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'qualification', 'id':'qualification','type':'text'}))
    professional_membership = forms.CharField(label='Professional Membership',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'professional_membership', 'id':'professional_membership','type':'text'}))  
    application_fee = forms.CharField(label='Fee',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'application_fee', 'id':'application_fee','type':'text', 'value':'50000', 'readonly':'readonly'}))
    email = forms.CharField(label='Email',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'email', 'id':'email','type':'text' }))
    previous_business_engagement =  forms.ChoiceField(label='Has the applicant been employed  in any gaming facility ', choices=BOOL_CHOICE, required=True, widget=forms.Select(attrs={'class': 'form-control', 'name':'previous_business_engagement', 'id':'previous_business_engagement','type':'select'}))
    name_of_the_employer = forms.CharField(label='If yes, specify employers name',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'name_of_the_employer', 'id':'name_of_the_employer','type':'text'}))
    crime_engagement = forms.ChoiceField(label='Has the applicant been convicted for any offence or crime, even though subject of pardon, amnesty, or other similar action', choices=BOOL_CHOICE, required=False, widget=forms.Select(attrs={'class': 'form-control', 'name':'crime_engagement', 'id':'crime_engagement','type':'select'}))
    crime_details = forms.CharField(label='Provide the particulars of the offence or crime',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'crime_details', 'id':'crime_details','type':'text'}))
    
    cv = forms.FileField(label='Cv',  required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'cv', 'id':'cv','type':'file' }))
    interpoal_clearance  = forms.FileField(label='Interpol clearance',  required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'interpoal_clearance', 'id':'interpoal_clearance','type':'file' }))
    national_id = forms.FileField(label='National ID ',  required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'national_id', 'id':'national_id','type':'file' }))
    passport = forms.FileField(label='Passport',  required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'passport', 'id':'passport','type':'file' }))
    work_permit = forms.FileField(label='Work Permit ',  required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'work_permit', 'id':'work_permit','type':'file' }))
    # ura 
    generate_prn = forms.BooleanField(label='Payment Registration Number (PRN)', required=True,  widget=forms.CheckboxInput(attrs={'class': 'form-check-input ', 'name':'generate_prn', 'id':'generate_prn','type':'checkbox'}))
    prn = forms.CharField(label='Payment Registration Number(PRN)',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'prn', 'id':'prn','type':'text','readonly':'readonly' }))
    error_code = forms.CharField(label='ErrorCode',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'error_code', 'id':'error_code','type':'hidden', }))
    error_desc = forms.CharField(label='ErrorDesc',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'error_desc', 'id':'error_desc','type':'hidden', }))
    payment_expiry_date = forms.CharField(label='ExpiryDate',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'payment_expiry_date', 'id':'payment_expiry_date','type':'hidden', }))
    search_code = forms.CharField(label='SearchCode',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'search_code', 'id':'search_code','type':'hidden', }))
    ura_district = forms.CharField(label='ura_district',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_district', 'id':'ura_district','type':'text', }))
    ura_county =  forms.CharField(label='ura_county',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_county', 'id':'ura_county','type':'text', }))
    ura_subcounty = forms.CharField(label='ura_subcounty',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_subcounty', 'id':'ura_subcounty','type':'text', }))
    ura_village = forms.CharField(label='ura_village',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_village', 'id':'ura_village','type':'text', }))


    class Meta:
        model = EmployeeLicence
        fields =  '__all__'


class EmployeeLicenceUpdateForm(forms.ModelForm):

    class Meta:
        model = EmployeeLicence
        fields =  [
            'inspection_authority_status',
            'inspection_authority_remarks',
            'forward_for_verification',
            
            'verification_authority_status',
            'verification_authority_remarks',
            'forward_for_approval',

            'approving_authority_status',
            'approved',

            'assigned_to_inspector',
            'manager_remarks', 
            'date_assigned',
            
        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeLicenceUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True


class PremisesForm(forms.ModelForm):

    operator_name = forms.CharField(label='Operator Name',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'operator_name','readonly': 'readonly', 'id':'operator_name','type':'text'}))
    premise_name = forms.CharField(label='Premise Name',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'premise_name', 'id':'premise_name','type':'text'}))
    trade_name = forms.CharField(label='Trade Name',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'trade_name', 'id':'trade_name','type':'text'}))
    location =  forms.CharField(label='Location ',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'location', 'id':'location','type':'text'}))
    building_name = forms.CharField(label='Building Name',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'building_name', 'id':'building_name','type':'text'}))
    plot_number = forms.CharField(label='Plot Number',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'plot_number', 'id':'plot_number','type':'text'}))
    town_council = forms.CharField(label='Town Council',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'town_council', 'id':'town_council','type':'text'}))
    municipality = forms.CharField(label='Municipality',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'municipality', 'id':'municipality','type':'text'}))
    district = forms.CharField(label='District',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'district', 'id':'district','type':'text'}))
    region = forms.CharField(label='Region',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'region', 'id':'region','type':'text'}))
    equipment_in_the_premise = forms.CharField(label='Equipment in the premise',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'equipment_in_the_premise', 'id':'equipment_in_the_premise','type':'text'}))
    number_of_gaming_devices = forms.CharField(label='Number of gaming devices',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'number_of_gaming_devices', 'id':'number_of_gaming_devices','type':'text'}))
    email = forms.CharField(label='email',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'email', 'id':'email','type':'text' }))
    inspection_fee = forms.CharField(label='Premise Inspection and approval fees',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'inspection_fee', 'id':'inspection_fee','type':'text', 'value':'1000000', 'readonly':'readonly'}))


    generate_prn = forms.BooleanField(label='Generate Payment Registration Number (PRN)', required=True,  widget=forms.CheckboxInput(attrs={'class': 'form-check-input custom-control-input',  'role':'switch',  'name':'generate_prn', 'id':'generate_prn','type':'checkbox'}))
    tin = forms.CharField(label='TIN of the Company',  required=True, widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'tin', 'id':'tin','type':'text' }))
    prn = forms.CharField(label='Payment Registration Number(PRN)',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'prn', 'id':'prn','type':'text', 'readonly': 'readonly'}))
    error_code = forms.CharField(label='error_code',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'error_code', 'id':'error_code','type':'hidden', }))
    error_desc = forms.CharField(label='error_desc',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'error_desc', 'id':'error_desc','type':'hidden', }))
    payment_expiry_date = forms.CharField(label='payment_expiry_date',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'payment_expiry_date', 'id':'payment_expiry_date','type':'hidden', }))
    # payment_registered_on = forms.CharField(label='payment_registered_on',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'payment_registered_on', 'id':'payment_registered_on','type':'hidden', }))   
    search_code = forms.CharField(label='search_code',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'search_code', 'id':'search_code','type':'hidden', }))
    ura_district = forms.CharField(label='ura_district',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_district', 'id':'ura_district','type':'text', }))
    ura_county =  forms.CharField(label='ura_county',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_county', 'id':'ura_county','type':'text', }))
    ura_subcounty = forms.CharField(label='ura_subcounty',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_subcounty', 'id':'ura_subcounty','type':'text', }))
    ura_village = forms.CharField(label='ura_village',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'ura_village', 'id':'ura_village','type':'text', }))


    class Meta:
        model = PremiseLicence
        
        # fields = [
        #     'operator_name',
        #     'premise_name',
        #     'location', 
        #     'building_name',
        #     'plot_number',
        #     'town_council',
        #     'municipality','district', 
        #     'region',
        #     'size',
        #     'equipment_in_the_premise',
        #     'number_of_gaming_devices', 
        #     'email'

        #     'inspection_fee',
            
        # ]
        fields = "__all__"


class PremiseLicenceUpdateForm(forms.ModelForm):

    operator_name = forms.CharField(label='Operator Name',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'operator_name', 'id':'operator_name','type':'text'}))


    class Meta:
        model = PremiseLicence

        # fields =  [
        #     'inspection_authority_status',
        #     'inspection_authority_remarks',
        #     'forward_for_verification',
        #     'inspection_report',

        #     'verification_authority_status',
        #     'verification_authority_remarks',
        #     'forward_for_approval',

        #     'approving_authority_status',
        #     'approved',
        # ]

        fields = "__all__"






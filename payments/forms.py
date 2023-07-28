from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from config.choices import *
from payments.models import *
from new.models import PrincipleLicence

class ApplicationFeePaymentForm(forms.ModelForm):    

    application_fee = forms.CharField(label='Application Fee', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'application_fee', 'id':'application_fee','type':'text', 'readonly':'readonly'}))
    tin = forms.CharField(label='Tin', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'tin', 'id':'tin','type':'text'}))

    generate_prn = forms.BooleanField(label='Generate', required=False,  widget=forms.CheckboxInput(attrs={'class': 'form-check-input ', 'name':'generate_prn', 'id':'generate_prn','type':'checkbox'}))
    prn = forms.CharField(label='payment Registration Number', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'prn', 'id':'prn','type':'text', 'readonly':'readonly'}))
    
    error_code = forms.CharField(label='error_code', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'error_code', 'id':'error_code','type':'hidden', 'readonly':'readonly'}))
    error_desc = forms.CharField(label='error_desc', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'error_desc', 'id':'error_desc','type':'hidden', 'readonly':'readonly'}))
    search_code = forms.CharField(label='search_code', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'search_code', 'id':'search_code','type':'hidden', 'readonly':'readonly'}))
    payment_expiry_date =  forms.CharField(label='payment_expiry_date', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'payment_expiry_date', 'id':'payment_expiry_date','type':'hidden', 'readonly':'readonly'}))
    
    class Meta:
        model = ApplicationFeePayments
       
        fields = [
            'tin',
            'application_fee',
            'error_code',
            'error_desc',
            'search_code',
            'payment_expiry_date',
            'generate_prn',
            'prn',
        
        ]
       

class LicenceFeePaymentForm(forms.ModelForm):
    
    licence_fee = forms.CharField(label='Licence Fee', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'licence_fee', 'id':'licence_fee','type':'text', 'readonly':'readonly'}))
    licence_fee_tin = forms.CharField(label='Tin', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'licence_fee_tin', 'id':'licence_fee_tin','type':'text'}))

    generate_prn_licence_fee = forms.BooleanField(label='Generate Payment Registration Number', required=False,  widget=forms.CheckboxInput(attrs={'class': 'form-check-input ', 'name':'generate_prn_licence_fee', 'id':'generate_prn_licence_fee','type':'checkbox'}))
    # generate_prn = forms.BooleanField(label='Generate', required=True,  widget=forms.CheckboxInput(attrs={'class': 'form-check-input ', 'name':'generate_prn', 'id':'generate_prn','type':'checkbox'}))

    licence_fee_prn = forms.CharField(label='', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'licence_fee_prn', 'id':'licence_fee_prn','type':'text', 'readonly':'readonly'}))
    
    licence_fee_error_code = forms.CharField(label='licence_fee_error_code', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'licence_fee_error_code', 'id':'licence_fee_error_code','type':'hidden', 'readonly':'readonly'}))
    licence_fee_error_desc = forms.CharField(label='licence_fee_error_desc', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'licence_fee_error_desc', 'id':'licence_fee_error_desc','type':'hidden', 'readonly':'readonly'}))
    licence_fee_search_code = forms.CharField(label='licence_fee_search_code', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'licence_fee_search_code', 'id':'licence_fee_search_code','type':'hidden', 'readonly':'readonly'}))
    payment_expiry_date =  forms.CharField(label='payment_expiry_date', required=False,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'payment_expiry_date', 'id':'payment_expiry_date','type':'hidden', 'readonly':'readonly'}))
    
    class Meta:
        model = LicenceFeePayments
       
        fields = [
            'licence_fee_tin',
            'generate_prn_licence_fee',

            'licence_fee_prn',
            'licence_fee_error_code',
            'licence_fee_error_desc',
            'licence_fee_search_code',

            'payment_expiry_date',
            'licence_fee'
        
        ]
       
    # def clean(self):
    #     cleaned_data = super(LicenceFeePaymentForm, self).clean()
    #     certificate_no = cleaned_data.get('principle_licence_certificate_number')
    #     if certificate_no:
    #         exists = PrincipleLicence.objects.filter(certificate_number=certificate_no).exists()
    #         if not exists:
    #             raise forms.ValidationError('The certificate number %s does not match our records.'%certificate_no)
    #     return cleaned_data


class PremiseLicencePaymentForm(forms.ModelForm):
    name_of_the_company = forms.CharField(label='Name of the company ',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'name_of_the_company', 'id':'name_of_the_company','type':'text', 'readonly':'readonly'}))
    email = forms.CharField(label='Companys Email',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'email', 'id':'email','type':'text', 'readonly':'readonly'}))
    licence_fee = forms.CharField(label='Licence Fee',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'licence_fee', 'id':'licence_fee','type':'text', 'value':'1000000', 'min':1000000, 'readonly':'readonly'}))
    number_of_premises = forms.IntegerField(label='Number of Premises',  required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'name':'nop', 'id':'nop','type':'number', 'min':1, 'readonly':'readonly' }))
    premise = forms.FileField(label='Premises attachment',  required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'name':'premise', 'id':'premise','type':'file' }))
    tin = forms.CharField(label='Tin', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'tin', 'id':'tin','type':'text'}))
    generate_prn = forms.BooleanField(label=' Payment Registration Number (PRN) ', required=True,  widget=forms.CheckboxInput(attrs={'class': 'form-check-input ', 'name':'generate_prn', 'id':'generate_prn','type':'checkbox'}))
    prn = forms.CharField(label='Payment Registration Number(PRN)',  required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'prn', 'id':'prn','type':'text','readonly':'readonly' }))
    error_code = forms.CharField(label='error_code', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'error_code', 'id':'error_code','type':'text', 'readonly':'readonly'}))
    error_desc = forms.CharField(label='error_desc', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'error_desc', 'id':'error_desc','type':'text', 'readonly':'readonly'}))
    search_code = forms.CharField(label='search_code', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'search_code', 'id':'search_code','type':'text', 'readonly':'readonly'}))
    expiry_date =  forms.CharField(label='expiry_date', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'expiry_date', 'id':'expiry_date','type':'text', 'readonly':'readonly'}))
    district = forms.CharField(label='district',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'district', 'id':'district','type':'text', }))
    county =  forms.CharField(label='county',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'county', 'id':'county','type':'text', }))
    subcounty = forms.CharField(label='subcounty',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'subcounty', 'id':'subcounty','type':'text', }))
    village = forms.CharField(label='village',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name':'village', 'id':'village','type':'text', }))


    class Meta:
        model = PremisePayment
        fields = '__all__'


class LicenceFeePaymentUpdateForm(forms.Form):

    class Meta:
        model = LicenceFeePayments
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LicenceFeePaymentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True


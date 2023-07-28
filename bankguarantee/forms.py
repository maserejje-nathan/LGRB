from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder

from new.models import *
from bankguarantee.models import *
from django.conf import settings

from config.choices import *
from account.models import *


class BankGuaranteeForm(forms.ModelForm):
    principle_licence_certificate_number = forms.CharField(label='Certificate Number', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'certificate_number', 'id':'certificate_number','type':'text'}))
    Name = forms.CharField(label='Name', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'name_of_the_company', 'id':'name_of_the_company','type':'text', 'readonly':'readonly'}))
    email = forms.EmailField(label='Email', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'email', 'id':'email','type':'text', 'readonly':'readonly'}))
    bank = forms.CharField(label='Issuing bank', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'bank', 'id':'bank','type':'text'}))
    bank_guarantee = forms.FileField(label='Bank Guarantee', required=True,  widget=forms.FileInput(attrs={'class': 'form-control ', 'name':'bankguarantee', 'id':'bankguarantee','type':'file'}))
    
    class Meta:
        model = BankGuarantee
        fields =  ['principle_licence_certificate_number','Name', 'email', 'bank', 'bank_guarantee']
        

    def clean(self):
        cleaned_data = super(BankGuaranteeForm, self).clean()
        certificate_no = cleaned_data.get('principle_licence_certificate_number')
        if certificate_no:
            exists = PrincipleLicence.objects.filter(certificate_number=certificate_no).exists()
            if not exists:
                raise forms.ValidationError('The certificate number %s does not match our records. Please proceed to apply.'%certificate_no)
        return cleaned_data
        

class BankGuaranteeUpdateForm(forms.Form):

    class Meta:
        model = BankGuarantee
        fields = [
            # verification officer
            'verification_authority_status', 
            'verification_authority_remarks', 
            'verified_by',
            'forward_for_approval',
            'date_verified', 

            # approving officer 
            'approving_authority_status', 
            'approving_authority_remarks',
            'date_approved' 
        ]

    def __init__(self, *args, **kwargs):
        super(BankGuaranteeUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True


# renewed

class RenewedBankGuaranteeForm(forms.ModelForm):
    principle_licence_certificate_number = forms.CharField(label='Certificate Number', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'certificate_number', 'id':'certificate_number','type':'text'}))
    Name = forms.CharField(label='Name', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'Name', 'id':'Name','type':'text'}))
    email = forms.EmailField(label='Email', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'bank', 'id':'bank','type':'text'}))
    bank = forms.CharField(label='Issuing bank', required=True,  widget=forms.TextInput(attrs={'class': 'form-control ', 'name':'bank', 'id':'bank','type':'text'}))
    bank_guarantee = forms.FileField(label='Bank Guarantee', required=True,  widget=forms.FileInput(attrs={'class': 'form-control ', 'name':'bankguarantee', 'id':'bankguarantee','type':'file'}))
    

    class Meta:
        model = BankGuarantee
        fields =  ['principle_licence_certificate_number','Name', 'email', 'bank', 'bank_guarantee']
        

    def clean(self):
        cleaned_data = super(BankGuaranteeForm, self).clean()
        certificate_no = cleaned_data.get('principle_licence_certificate_number')
        if certificate_no:
            exists = PrincipleLicence.objects.filter(certificate_number=certificate_no).exists()
            if not exists:
                raise forms.ValidationError('The certificate number %s does not match our records. Please proceed to apply.'%certificate_no)
        return cleaned_data
        

class RenewedBankGuaranteeUpdateForm(forms.Form):

    class Meta:
        model = BankGuarantee
        fields = [
            # verification officer
            'verification_authority_status', 
            'verification_authority_remarks', 
            'verified_by',
            'forward_for_approval',
            'date_verified', 

            # approving officer 
            'approving_authority_status', 
            'approving_authority_remarks',
            'approved', 
            'date_approved' 
        ]

    def __init__(self, *args, **kwargs):
        super(BankGuaranteeUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True


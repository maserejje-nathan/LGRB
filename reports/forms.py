from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
from django.db.models.query import QuerySet

from new.models import *
from django.conf import settings
from config.choices import *
from account.models import *
from datetime import  datetime 
from config.choices import * 


# class EmployeeFilterForm(forms.Form):
#     # pass 

#     # accounts = EmployeeLicence.objects.all()
#     accounts = PrincipleLicence.objects.select_related('applicant').distinct( 'applicant__first_name', 'applicant__last_name')
    
#     # choices = [( f"{account.applicant.first_name} - {account.applicant.last_name} ") for account in accounts]
#     choices = [(
#         account.email, f"{account.applicant.first_name} - {account.applicant.last_name} ") for account in accounts]
#     # choices = [(email, f"{applicant.first_name} - {applicant.last_name} ") for email, applicant in accounts.values_list('email', 'applicant')]

#     print(choices)
#     operator_name = forms.ChoiceField(
#         label='Select company', 
#         choices = choices,
#         required=True, 
#         widget=forms.Select(attrs={'class': 'form-control first_name', 'name':'first_name', 'id':'first_name','type':'select'}))





class EmployeeFilterForm(forms.Form):
 
    username = Account.objects.filter(  role = "client").values_list('id', 'first_name', 'last_name')
    choices = [(id, f"{first_name} {last_name}") for id, first_name, last_name in username]
    
    name_of_the_company = forms.ChoiceField(
        label='Select operator', 
        choices = choices, required=True, 
        widget=forms.Select(attrs={'class': 'form-control ', 'name':'name_of_the_company', 'id':'name_of_the_company','type':'select'}))
    
    year = forms.ChoiceField(
        label='Select year', 
        choices = year_choices, required=True, 
        widget=forms.Select(attrs={'class': 'form-control ', 'name':'year', 'id':'year','type':'select'}))


class YearFilterForm(forms.Form):
 
    year = forms.ChoiceField(
        label='Select year', 
        choices = year_choices, required=True, 
        widget=forms.Select(attrs={'class': 'form-control ', 'name':'year', 'id':'year','type':'select'}))


class VerificationRecomendationForm(forms.Form):

    verification_status  = forms.ChoiceField(
        label='management recommendation status', 
        choices = verification_choices, required=True, 
        widget=forms.Select(attrs={'class': 'form-control ', 'name':'verification_status', 'id':'verification_status','type':'select'}))
    
    licencing_perriod = forms.ChoiceField(
            label='Select licensing year', 
            choices = year_choices, required=True, 
            widget=forms.Select(attrs={'class': 'form-control ', 'name':'year', 'id':'year','type':'select'}))


class ApprovalForm(forms.Form):

    approval_status  = forms.ChoiceField(
        label='Board approval status', 
        choices = approved_choices, required=True, 
        widget=forms.Select(attrs={'class': 'form-control ', 'name':'approval_status', 'id':'approval_status','type':'select'}))
    
   

